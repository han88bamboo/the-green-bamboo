<template>
  <div class="poll-card-container" :class="{ 'mobile-collapsed': isMobileCollapsed }">
    <!-- Collapse Header for Logged-in Users (visible when polls exist OR user is creator) -->
    <div v-if="(polls.length > 0 || isCreator) && currentUserId" class="mobile-collapse-header" @click="toggleMobileCollapse">
      <div class="mobile-header-content">
        <div class="mobile-header-info">
          <h6 class="mobile-poll-title">
            <div class="mobile-poll-title-content">
              <span class="mobile-poll-text">
                <i class="bi bi-bar-chart-fill poll-icon"></i>
                <span class="poll-label">Poll:</span> 
                <span v-if="polls.length > 0">{{ currentPoll.title }}</span>
                <span v-else>No polls yet</span>
              </span>
            </div>
          </h6>
          <span class="mobile-poll-count" v-if="polls.length > 0">{{ currentPollIndex + 1 }} / {{ polls.length }}</span>
          <span class="mobile-poll-count" v-else>0 polls</span>
        </div>
        <div class="mobile-collapse-icon">
          <svg v-if="isMobileCollapsed" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Collapse Header for Non-Logged-in Users (triggers signup popup) -->
    <div v-if="(polls.length > 0 || isCreator) && !currentUserId" class="mobile-collapse-header" @click="triggerSignUpPopup">
      <div class="mobile-header-content">
        <div class="mobile-header-info">
          <h6 class="mobile-poll-title">
            <div class="mobile-poll-title-content">
              <span class="mobile-poll-text">
                <i class="bi bi-bar-chart-fill poll-icon"></i>
                <span class="poll-label">Poll:</span> 
                <span v-if="polls.length > 0">{{ currentPoll.title }}</span>
                <span v-else>No polls yet</span>
              </span>
            </div>
          </h6>
          <span class="mobile-poll-count" v-if="polls.length > 0">{{ currentPollIndex + 1 }} / {{ polls.length }}</span>
          <span class="mobile-poll-count" v-else>0 polls</span>
        </div>
        <div class="mobile-collapse-icon">
          <i class="bi bi-box-arrow-in-right" style="font-size: 1.2rem; color: #007bff;" title="Sign up to participate"></i>
        </div>
      </div>
    </div>

    <!-- Poll Content Container -->
    <div class="poll-content-container" :class="{ 'collapsed': isMobileCollapsed }">
    <!-- Poll Cards Carousel -->
    <div class="poll-carousel" v-if="polls.length > 0">
      <!-- Navigation Arrows -->
      <button 
        v-if="polls.length > 1"
        class="carousel-arrow carousel-arrow-left" 
        @click="previousPoll"
        :disabled="currentPollIndex === 0"
      >
        <i class="bi bi-chevron-left"></i>
      </button>

      <!-- Poll Card -->
      <div class="poll-card">
        <div class="poll-header">
          <!-- Header Navigation Arrow Left -->
          <button 
            v-if="polls.length > 1"
            class="header-nav-arrow header-nav-arrow-left" 
            @click="previousPoll"
            :disabled="currentPollIndex === 0"
            title="Previous Poll"
          >
            <i class="bi bi-chevron-left"></i>
          </button>

          <div class="poll-title-section">
            <h4 class="poll-title">
              <div class="poll-title-content">
                <span class="poll-title-text">
                <i class="bi bi-bar-chart-fill poll-icon"></i>
                <span class="poll-label">Poll:</span> {{ currentPoll.title }}</span>
              </div>
            </h4>
            <p class="poll-question">{{ currentPoll.questionText }}</p>
          </div>

          <!-- Header Navigation Arrow Right -->
          <button 
            v-if="polls.length > 1"
            class="header-nav-arrow header-nav-arrow-right" 
            @click="nextPoll"
            :disabled="currentPollIndex === polls.length - 1"
            title="Next Poll"
          >
            <i class="bi bi-chevron-right"></i>
          </button>
          
          <!-- Creator Controls (only visible to poll creator) -->
          <div v-if="isCreator" class="poll-controls">
            <button 
              class="btn btn-sm btn-outline-secondary me-2" 
              @click="toggleVisibility(currentPoll)"
              :title="currentPoll.isVisible ? 'Hide Poll' : 'Show Poll'"
            >
              <i :class="currentPoll.isVisible ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
            <button 
              class="btn btn-sm btn-outline-danger" 
              @click="deletePoll(currentPoll.id)"
              title="Delete Poll"
            >
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>

        <!-- Poll Status Indicators -->
        <div class="poll-status">
          <span v-if="!currentPoll.isActive" class="badge bg-secondary me-2">Closed</span>
          <span v-if="!currentPoll.isVisible" class="badge  me-2" style="background-color:#596269;"><i class="bi bi-eye"></i> Hidden</span>
          <span v-if="currentPoll.expiresAt" class="badge me-2" :class="getExpirationBadgeClass(currentPoll.expiresAt)">
            {{ formatRelativeTime(currentPoll.expiresAt) }}
          </span>
        </div>

        <!-- Poll Content Based on Type -->
        <div class="poll-content mt-3">
          <!-- User Status Message -->
          <div v-if="!canUserVote && currentUserId" class="user-status-message mb-3">
            <div v-if="isCreator" class="alert alert-secondary">
              <i class="bi bi-person-gear me-2"></i>
              <strong>Poll Creator:</strong> You created this poll.
            </div>
            <div v-else-if="currentUserType !== 'user'" class="alert alert-info">
              <i class="bi bi-building me-2"></i>
              <strong>Business Account:</strong> Only ordinary users can participate in polls. You can view the results below.
            </div>
            <div v-else-if="currentUserHasVoted" class="alert alert-success">
              <i class="bi bi-check-circle-fill me-2"></i>
              <strong>Thank you!</strong> Here's what you voted.
            </div>
          </div>
          
          <!-- Multiple Choice Single Selection -->
          <div v-if="currentPoll.questionType === 'multiple_choice_single_selection'">
            <p class="mb-3 mobile-rating-smaller-text-2">Select one option, then click 'SUBMIT':</p>
            
            <!-- Voting Interface (only for ordinary users who can vote) -->
            <div v-if="canUserVote" class="poll-voting">
              <div 
                v-for="option in currentPoll.options" 
                :key="option.id"
                class="poll-option single-choice"
                @click="selectSingleOption(currentPoll.id, option.id)"
                :class="{ 'selected': selectedSingleOption === option.id }"
              >
                <div class="option-radio">
                  <input 
                    type="radio" 
                    :name="`poll-${currentPoll.id}`" 
                    :value="option.id"
                    v-model="selectedSingleOption"
                  >
                </div>
                <span class="option-text mobile-rating-smaller-text-2">{{ option.optionText }}</span>
              </div>
              <button 
                class="btn primary-btn-less-round-blue fw-bold mobile-rating-smaller-text-2 mt-2" 
                @click="submitSingleChoice(currentPoll.id)"
                :disabled="!selectedSingleOption"
              >
                Submit Vote
              </button>
            </div>
            
            <!-- Results View (for everyone else) -->
            <div v-if="shouldShowResults" class="poll-results">
              <!-- User's Previous Vote Indicator -->
              <div v-if="currentUserResponse" class="user-vote-indicator mb-3 mobile-rating-smaller-text-2">
                <div class="alert alert-info">
                  <i class="bi bi-check-circle-fill me-2"></i>
                  <strong>You voted for:</strong> 
                  {{ getUserSelectedOptionText(currentUserResponse.selectedOptionIds) }}
                </div>
              </div>
              
              <div 
                v-for="option in currentPoll.options" 
                :key="option.id"
                class="result-option"
              >
                <div class="result-header">
                  <span class="option-text mobile-rating-smaller-text-2">
                    {{ option.optionText }}
                    <i v-if="userVotedForOption(currentPoll.id, option.id)" 
                       class="bi bi-check-circle-fill text-success ms-2" 
                       title="You voted for this option"></i>
                  </span>
                  <!-- Show percentage only for creators -->
                  <span v-if="isCreator" class="percentage">{{ getOptionPercentage(currentPoll.id, option.id) }}%</span>
                  <!-- Commented out: Regular users don't see percentages
                  <span class="percentage">{{ getOptionPercentage(currentPoll.id, option.id) }}%</span>
                  -->
                </div>
                <!-- Show progress bars only for creators -->
                <div v-if="isCreator" class="progress">
                  <div 
                    class="progress-bar" 
                    :style="{ width: getOptionPercentage(currentPoll.id, option.id) + '%' }"
                    :class="{ 'user-voted': userVotedForOption(currentPoll.id, option.id) }"
                  ></div>
                </div>
                <!-- Commented out: Regular users don't see progress bars
                <div class="progress">
                  <div 
                    class="progress-bar" 
                    :style="{ width: getOptionPercentage(currentPoll.id, option.id) + '%' }"
                    :class="{ 'user-voted': userVotedForOption(currentPoll.id, option.id) }"
                  ></div>
                </div>
                -->
              </div>
              <div class="total-votes">{{ getTotalVotes(currentPoll.id) }} votes</div>
              
              <!-- Creator-Only Detailed Responses Section -->
              <div v-if="isCreator" class="creator-responses-section mt-4">
                <div class="detailed-responses-header">
                  <button 
                    class="btn btn-success btn-sm me-2"
                    @click="openRandomPickWinnerModal(currentPoll.id)"
                    :disabled="getTotalVotes(currentPoll.id) === 0"
                  >
                    <i class="bi bi-trophy me-2"></i>
                    Randomly Pick A Winner
                  </button>
                  <button 
                    class="btn btn-outline-info btn-sm"
                    @click="toggleDetailedResponses(currentPoll.id)"
                    :disabled="loadingDetailedResponses"
                  >
                    <i class="bi bi-people me-2"></i>
                    <span v-if="!showDetailedResponses[currentPoll.id]">
                      View Detailed Responses
                      <span v-if="loadingDetailedResponses" class="spinner-border spinner-border-sm ms-2"></span>
                    </span>
                    <span v-else>Hide Detailed Responses</span>
                  </button>
                </div>
                
                <div v-if="showDetailedResponses[currentPoll.id]" class="detailed-responses-content mt-3">
                  <div v-if="detailedResponses[currentPoll.id] && detailedResponses[currentPoll.id].length > 0" class="responses-list">
                    <h6 class="responses-title">
                      <i class="bi bi-person-lines-fill me-2"></i>
                      Individual Responses ({{ detailedResponses[currentPoll.id].length }})
                    </h6>
                    
                    <div 
                      v-for="response in detailedResponses[currentPoll.id]" 
                      :key="response.responseId"
                      class="response-item"
                    >
                      <div class="response-header">
                        <div class="respondent-info">
                          <span class="respondent-name">{{ response.respondentDisplayName }}</span>
                          <span class="respondent-username">@{{ response.respondentUsername }}</span>
                        </div>
                        <div class="response-timestamp" v-if="response.createdAt">
                          {{ formatResponseDate(response.createdAt) }}
                        </div>
                      </div>
                      
                      <div class="response-content">
                        <!-- For Multiple Choice Single Selection -->
                        <div v-if="currentPoll.questionType === 'multiple_choice_single_selection' && response.selectedOptionIds">
                          <span class="response-label">Selected:</span>
                          <span class="response-value">{{ getOptionTextById(response.selectedOptionIds[0]) }}</span>
                        </div>
                        
                        <!-- For Multiple Choice Multi Selection -->
                        <div v-if="currentPoll.questionType === 'multiple_choice_multi_selection' && response.selectedOptionIds">
                          <span class="response-label">Selected:</span>
                          <div class="multi-selection-response">
                            <span 
                              v-for="optionId in response.selectedOptionIds" 
                              :key="optionId"
                              class="badge bg-primary me-1"
                            >
                              {{ getOptionTextById(optionId) }}
                            </span>
                          </div>
                        </div>
                        
                        <!-- For Rating Scale -->
                        <div v-if="currentPoll.questionType === 'rating_scale' && response.ratingValue">
                          <span class="response-label">Rating:</span>
                          <span class="response-value rating-response">
                            {{ response.ratingValue }}/5
                            <span class="rating-stars ms-2">
                              <i 
                                v-for="star in 5" 
                                :key="star"
                                :class="star <= response.ratingValue ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'"
                              ></i>
                            </span>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-else-if="!loadingDetailedResponses" class="no-responses">
                    <div class="text-center text-muted py-3">
                      <i class="bi bi-inbox mb-2" style="font-size: 2rem;"></i>
                      <p class="mb-0 mobile-rating-smaller-text-2">No responses yet for this poll.</p>
                    </div>
                  </div>
                  
                  <div v-if="loadingDetailedResponses" class="loading-responses text-center py-3">
                    <div class="spinner-border text-primary" role="status">
                      <span class="visually-hidden">Loading responses...</span>
                    </div>
                    <p class="text-muted mt-2 mb-0">Loading detailed responses...</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Multiple Choice Multi Selection -->
          <div v-if="currentPoll.questionType === 'multiple_choice_multi_selection'">
             <p class="mb-3 mobile-rating-smaller-text-2">Select all that apply, then click 'SUBMIT':</p>
             
            <!-- Voting Interface (only for ordinary users who can vote) -->
            <div v-if="canUserVote" class="poll-voting">
              <div 
                v-for="option in currentPoll.options" 
                :key="option.id"
                class="poll-option multi-choice"
                @click="toggleMultiOption(option.id)"
                :class="{ 'selected': selectedMultiOptions.includes(option.id) }"
              >
                <div class="option-checkbox">
                  <input 
                    type="checkbox" 
                    :value="option.id"
                    v-model="selectedMultiOptions"
                  >
                </div>
                <span class="option-text mobile-rating-smaller-text-2">{{ option.optionText }}</span>
              </div>
              <button 
                class="btn primary-btn-less-round-blue fw-bold mobile-rating-smaller-text-2 mt-2" 
                @click="submitMultiChoice(currentPoll.id)"
                :disabled="selectedMultiOptions.length === 0"
              >
                Submit Vote
              </button>
            </div>
            
            <!-- Results View (for everyone else) -->
            <div v-if="shouldShowResults" class="poll-results">
              <!-- User's Previous Vote Indicator -->
              <div v-if="currentUserResponse" class="user-vote-indicator mb-3 mobile-rating-smaller-text-2">
                <div class="alert alert-info">
                  <i class="bi bi-check-circle-fill me-2"></i>
                  <strong>You voted for:</strong> 
                  {{ getUserSelectedOptionsText(currentUserResponse.selectedOptionIds) }}
                </div>
              </div>
              
              <div 
                v-for="option in currentPoll.options" 
                :key="option.id"
                class="result-option"
              >
                <div class="result-header">
                  <span class="option-text mobile-rating-smaller-text-2">
                    {{ option.optionText }}
                    <i v-if="userVotedForOption(currentPoll.id, option.id)" 
                       class="bi bi-check-circle-fill text-success ms-2" 
                       title="You voted for this option"></i>
                  </span>
                  <!-- Show percentage only for creators -->
                  <span v-if="isCreator" class="percentage">{{ getOptionPercentage(currentPoll.id, option.id) }}%</span>
                  <!-- Commented out: Regular users don't see percentages
                  <span class="percentage">{{ getOptionPercentage(currentPoll.id, option.id) }}%</span>
                  -->
                </div>
                <!-- Show progress bars only for creators -->
                <div v-if="isCreator" class="progress">
                  <div 
                    class="progress-bar" 
                    :style="{ width: getOptionPercentage(currentPoll.id, option.id) + '%' }"
                    :class="{ 'user-voted': userVotedForOption(currentPoll.id, option.id) }"
                  ></div>
                </div>
                <!-- Commented out: Regular users don't see progress bars
                <div class="progress">
                  <div 
                    class="progress-bar" 
                    :style="{ width: getOptionPercentage(currentPoll.id, option.id) + '%' }"
                    :class="{ 'user-voted': userVotedForOption(currentPoll.id, option.id) }"
                  ></div>
                </div>
                -->
              </div>
              <div class="total-votes">{{ getTotalVotes(currentPoll.id) }} votes</div>
              
              <!-- Creator-Only Detailed Responses Section -->
              <div v-if="isCreator" class="creator-responses-section mt-4">
                <div class="detailed-responses-header">
                  <button 
                    class="btn btn-success btn-sm me-2"
                    @click="openRandomPickWinnerModal(currentPoll.id)"
                    :disabled="getTotalVotes(currentPoll.id) === 0"
                  >
                    <i class="bi bi-trophy me-2"></i>
                    Randomly Pick A Winner
                  </button>
                  <button 
                    class="btn btn-outline-info btn-sm"
                    @click="toggleDetailedResponses(currentPoll.id)"
                    :disabled="loadingDetailedResponses"
                  >
                    <i class="bi bi-people me-2"></i>
                    <span v-if="!showDetailedResponses[currentPoll.id]">
                      View Detailed Responses
                      <span v-if="loadingDetailedResponses" class="spinner-border spinner-border-sm ms-2"></span>
                    </span>
                    <span v-else>Hide Detailed Responses</span>
                  </button>
                </div>
                
                <div v-if="showDetailedResponses[currentPoll.id]" class="detailed-responses-content mt-3">
                  <div v-if="detailedResponses[currentPoll.id] && detailedResponses[currentPoll.id].length > 0" class="responses-list">
                    <h6 class="responses-title">
                      <i class="bi bi-person-lines-fill me-2"></i>
                      Individual Responses ({{ detailedResponses[currentPoll.id].length }})
                    </h6>
                    
                    <div 
                      v-for="response in detailedResponses[currentPoll.id]" 
                      :key="response.responseId"
                      class="response-item"
                    >
                      <div class="response-header">
                        <div class="respondent-info">
                          <span class="respondent-name">{{ response.respondentDisplayName }}</span>
                          <span class="respondent-username">@{{ response.respondentUsername }}</span>
                        </div>
                        <div class="response-timestamp" v-if="response.createdAt">
                          {{ formatResponseDate(response.createdAt) }}
                        </div>
                      </div>
                      
                      <div class="response-content">
                        <!-- For Multiple Choice Single Selection -->
                        <div v-if="currentPoll.questionType === 'multiple_choice_single_selection' && response.selectedOptionIds">
                          <span class="response-label">Selected:</span>
                          <span class="response-value">{{ getOptionTextById(response.selectedOptionIds[0]) }}</span>
                        </div>
                        
                        <!-- For Multiple Choice Multi Selection -->
                        <div v-if="currentPoll.questionType === 'multiple_choice_multi_selection' && response.selectedOptionIds">
                          <span class="response-label">Selected:</span>
                          <div class="multi-selection-response">
                            <span 
                              v-for="optionId in response.selectedOptionIds" 
                              :key="optionId"
                              class="badge bg-primary me-1"
                            >
                              {{ getOptionTextById(optionId) }}
                            </span>
                          </div>
                        </div>
                        
                        <!-- For Rating Scale -->
                        <div v-if="currentPoll.questionType === 'rating_scale' && response.ratingValue">
                          <span class="response-label">Rating:</span>
                          <span class="response-value rating-response">
                            {{ response.ratingValue }}/5
                            <span class="rating-stars ms-2">
                              <i 
                                v-for="star in 5" 
                                :key="star"
                                :class="star <= response.ratingValue ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'"
                              ></i>
                            </span>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-else-if="!loadingDetailedResponses" class="no-responses">
                    <div class="text-center text-muted py-3">
                      <i class="bi bi-inbox mb-2" style="font-size: 2rem;"></i>
                      <p class="mb-0">No responses yet for this poll.</p>
                    </div>
                  </div>
                  
                  <div v-if="loadingDetailedResponses" class="loading-responses text-center py-3">
                    <div class="spinner-border text-primary" role="status">
                      <span class="visually-hidden">Loading responses...</span>
                    </div>
                    <p class="text-muted mt-2 mb-0">Loading detailed responses...</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Rating Scale -->
          <div v-if="currentPoll.questionType === 'rating_scale'">
            
            <!-- Voting Interface (only for ordinary users who can vote) -->
            <div v-if="canUserVote" class="poll-voting">
              <div class="rating-scale">
                <div class="rating-labels d-flex justify-content-center mb-1">
                    <p>Select from 1 to 5:</p>
                </div>
                <div class="rating-options">
                  <div 
                    v-for="rating in [1, 2, 3, 4, 5]" 
                    :key="rating"
                    class="rating-option"
                    @click="selectRating(currentPoll.id, rating)"
                    :class="{ 'selected': selectedRating === rating }"
                  >
                    <div class="rating-circle">{{ rating }}</div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Results View (for everyone else) -->
            <div v-if="shouldShowResults" class="poll-results rating-results">
              <!-- User's Previous Rating Indicator -->
              <div v-if="currentUserResponse" class="user-vote-indicator mb-3 mobile-rating-smaller-text-2">
                <div class="alert alert-info">
                  <i class="bi bi-star-fill me-2"></i>
                  <strong>You rated:</strong> 
                  {{ currentUserResponse.ratingValue }}/5 stars
                </div>
              </div>
              
              <!-- Show aggregate rating data only for creators -->
              <div v-if="isCreator" class="average-rating">
                <div class="rating-display">
                  <span class="rating-number">{{ getAverageRating(currentPoll.id) }}</span>
                  <span class="rating-scale-text">/5</span>
                </div>
                <div class="rating-breakdown">
                  <div 
                    v-for="rating in [5, 4, 3, 2, 1]" 
                    :key="rating"
                    class="rating-bar"
                  >
                    <span class="rating-label">
                      {{ rating }}
                      <i v-if="currentUserResponse && currentUserResponse.ratingValue === rating" 
                         class="bi bi-check-circle-fill ms-1" 
                         title="Your rating"></i>
                    </span>
                    <div class="progress">
                      <div 
                        class="progress-bar" 
                        :style="{ width: getRatingPercentage(currentPoll.id, rating) + '%' }"
                        :class="{ 'user-voted': currentUserResponse && currentUserResponse.ratingValue === rating }"
                      ></div>
                    </div>
                    <span class="rating-count">{{ getRatingCount(currentPoll.id, rating) }}</span>
                  </div>
                </div>
              </div>
              <!-- Commented out: Regular users don't see aggregate rating data
              <div class="average-rating">
                <div class="rating-display">
                  <span class="rating-number">{{ getAverageRating(currentPoll.id) }}</span>
                  <span class="rating-scale-text">/5</span>
                </div>
                <div class="rating-breakdown">
                  <div 
                    v-for="rating in [5, 4, 3, 2, 1]" 
                    :key="rating"
                    class="rating-bar"
                  >
                    <span class="rating-label">
                      {{ rating }}
                      <i v-if="currentUserResponse && currentUserResponse.ratingValue === rating" 
                         class="bi bi-check-circle-fill ms-1" 
                         title="Your rating"></i>
                    </span>
                    <div class="progress">
                      <div 
                        class="progress-bar" 
                        :style="{ width: getRatingPercentage(currentPoll.id, rating) + '%' }"
                        :class="{ 'user-voted': currentUserResponse && currentUserResponse.ratingValue === rating }"
                      ></div>
                    </div>
                    <span class="rating-count">{{ getRatingCount(currentPoll.id, rating) }}</span>
                  </div>
                </div>
              </div>
              -->
              
              <!-- Show simple rating display for regular users -->
              <div v-if="!isCreator" class="user-rating-display">
                <div class="rating-stars-display">
                  <span class="rating-label-simple">Rating Scale: 1-5 stars</span>
                  <div class="user-rating-stars mt-2">
                    <i 
                      v-for="star in 5" 
                      :key="star"
                      :class="currentUserResponse && star <= currentUserResponse.ratingValue 
                        ? 'bi bi-star-fill text-warning' 
                        : 'bi bi-star text-muted'"
                      style="font-size: 1.5rem; margin-right: 4px;"
                    ></i>
                    <span v-if="currentUserResponse" class="ms-2 text-muted">
                      ({{ currentUserResponse.ratingValue }}/5)
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="total-votes">{{ getTotalVotes(currentPoll.id) }} votes</div>
              
              <!-- Creator-Only Detailed Responses Section -->
              <div v-if="isCreator" class="creator-responses-section mt-4">
                <div class="detailed-responses-header">
                  <button 
                    class="btn btn-success btn-sm me-2"
                    @click="openRandomPickWinnerModal(currentPoll.id)"
                    :disabled="getTotalVotes(currentPoll.id) === 0"
                  >
                    <i class="bi bi-trophy me-2"></i>
                    Randomly Pick A Winner
                  </button>
                  <button 
                    class="btn btn-outline-info btn-sm"
                    @click="toggleDetailedResponses(currentPoll.id)"
                    :disabled="loadingDetailedResponses"
                  >
                    <i class="bi bi-people me-2"></i>
                    <span v-if="!showDetailedResponses[currentPoll.id]">
                      View Detailed Responses
                      <span v-if="loadingDetailedResponses" class="spinner-border spinner-border-sm ms-2"></span>
                    </span>
                    <span v-else>Hide Detailed Responses</span>
                  </button>
                </div>
                
                <div v-if="showDetailedResponses[currentPoll.id]" class="detailed-responses-content mt-3">
                  <div v-if="detailedResponses[currentPoll.id] && detailedResponses[currentPoll.id].length > 0" class="responses-list">
                    <h6 class="responses-title">
                      <i class="bi bi-person-lines-fill me-2"></i>
                      Individual Responses ({{ detailedResponses[currentPoll.id].length }})
                    </h6>
                    
                    <div 
                      v-for="response in detailedResponses[currentPoll.id]" 
                      :key="response.responseId"
                      class="response-item"
                    >
                      <div class="response-header">
                        <div class="respondent-info">
                          <span class="respondent-name">{{ response.respondentDisplayName }}</span>
                          <span class="respondent-username">@{{ response.respondentUsername }}</span>
                        </div>
                        <div class="response-timestamp" v-if="response.createdAt">
                          {{ formatResponseDate(response.createdAt) }}
                        </div>
                      </div>
                      
                      <div class="response-content">
                        <!-- For Multiple Choice Single Selection -->
                        <div v-if="currentPoll.questionType === 'multiple_choice_single_selection' && response.selectedOptionIds">
                          <span class="response-label">Selected:</span>
                          <span class="response-value">{{ getOptionTextById(response.selectedOptionIds[0]) }}</span>
                        </div>
                        
                        <!-- For Multiple Choice Multi Selection -->
                        <div v-if="currentPoll.questionType === 'multiple_choice_multi_selection' && response.selectedOptionIds">
                          <span class="response-label">Selected:</span>
                          <div class="multi-selection-response">
                            <span 
                              v-for="optionId in response.selectedOptionIds" 
                              :key="optionId"
                              class="badge bg-primary me-1"
                            >
                              {{ getOptionTextById(optionId) }}
                            </span>
                          </div>
                        </div>
                        
                        <!-- For Rating Scale -->
                        <div v-if="currentPoll.questionType === 'rating_scale' && response.ratingValue">
                          <span class="response-label">Rating:</span>
                          <span class="response-value rating-response">
                            {{ response.ratingValue }}/5
                            <span class="rating-stars ms-2">
                              <i 
                                v-for="star in 5" 
                                :key="star"
                                :class="star <= response.ratingValue ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'"
                              ></i>
                            </span>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-else-if="!loadingDetailedResponses" class="no-responses">
                    <div class="text-center text-muted py-3">
                      <i class="bi bi-inbox mb-2" style="font-size: 2rem;"></i>
                      <p class="mb-0">No responses yet for this poll.</p>
                    </div>
                  </div>
                  
                  <div v-if="loadingDetailedResponses" class="loading-responses text-center py-3">
                    <div class="spinner-border text-primary" role="status">
                      <span class="visually-hidden">Loading responses...</span>
                    </div>
                    <p class="text-muted mt-2 mb-0">Loading detailed responses...</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Poll Navigation Info -->
        <div v-if="polls.length > 1" class="poll-navigation-info">
          <span class="poll-counter">{{ currentPollIndex + 1 }} / {{ polls.length }}</span>
        </div>
      </div>

      <!-- Navigation Arrows -->
      <button 
        v-if="polls.length > 1"
        class="carousel-arrow carousel-arrow-right" 
        @click="nextPoll"
        :disabled="currentPollIndex === polls.length - 1"
      >
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>

    <!-- Create Poll Button (for creators) -->
    <div v-if="isCreator" class="create-poll-section">
      <button class="btn btn-primary w-100" @click="showCreateModal = true">
        <i class="bi bi-plus-lg me-2"></i>
        <span v-if="polls.length === 0">
          Create your first poll!
        </span>
        <span v-else>Create Another Poll</span>
      </button>
    </div>

    <!-- Random Winner Modal -->
    <div 
      v-if="showRandomWinnerModal" 
      class="modal fade show" 
      style="display: block; background-color: rgba(0,0,0,0.5);"
      @click.self="closeRandomWinnerModal"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-trophy-fill text-warning me-2"></i>
              Random Winner Selection
            </h5>
            <button type="button" class="btn-close" @click="closeRandomWinnerModal"></button>
          </div>
          <div class="modal-body">
            <!-- Loading State -->
            <div v-if="randomWinnerLoading" class="winner-loading-container">
              <div class="lottery-animation">
                <div class="lottery-spinner"></div>
                <div class="lottery-balls">
                  <div class="lottery-ball"></div>
                  <div class="lottery-ball"></div>
                  <div class="lottery-ball"></div>
                </div>
              </div>
              <p class="loading-text mt-4">Selecting a random winner...</p>
            </div>

            <!-- Winner Display -->
            <div v-else-if="randomWinner" class="winner-display">
              <div class="winner-announcement">
                <div class="confetti">🎉</div>
                <h3 class="winner-title">Congratulations!</h3>
                <div class="winner-card">
                  <div class="winner-icon">
                    <i class="bi bi-person-circle"></i>
                  </div>
                  <div class="winner-info">
                    <h4 class="winner-name">{{ randomWinner.respondentDisplayName || randomWinner.respondentUsername }}</h4>
                    <p class="winner-username">@{{ randomWinner.respondentUsername }}</p>
                  </div>
                </div>

                <!-- Display their response -->
                <div class="winner-response mt-4">
                  <h6 class="response-header">Their Response:</h6>
                  
                  <!-- Multiple Choice Response -->
                  <div v-if="randomWinner.selectedOptionsText && randomWinner.selectedOptionsText.length > 0" class="response-content">
                    <div v-for="(optionText, index) in randomWinner.selectedOptionsText" :key="index" class="response-option">
                      <i class="bi bi-check-circle-fill text-success me-2"></i>
                      {{ optionText }}
                    </div>
                  </div>

                  <!-- Rating Response -->
                  <div v-else-if="randomWinner.ratingValue" class="response-content">
                    <div class="rating-display-winner">
                      <i 
                        v-for="star in 5" 
                        :key="star"
                        class="bi"
                        :class="star <= randomWinner.ratingValue ? 'bi-star-fill text-warning' : 'bi-star text-muted'"
                      ></i>
                      <span class="ms-2">({{ randomWinner.ratingValue }} out of 5)</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- No Responses State -->
            <div v-else-if="randomWinnerError" class="no-winner-state">
              <div class="no-winner-icon">
                <i class="bi bi-inbox"></i>
              </div>
              <p class="no-winner-text">{{ randomWinnerError }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeRandomWinnerModal">Close</button>
            <button 
              v-if="randomWinner"
              type="button" 
              class="btn btn-success" 
              @click="pickAnotherWinner"
            >
              <i class="bi bi-arrow-repeat me-2"></i>
              Pick Another Winner
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Poll Modal -->
    <div 
      v-if="showCreateModal" 
      class="modal fade show" 
      style="display: block; background-color: rgba(0,0,0,0.5);"
      @click.self="closeCreateModal"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Poll</h5>
            <button type="button" class="btn-close" @click="closeCreateModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createPoll">
              <!-- Poll Title -->
              <div class="mb-3">
                <label class="form-label text-start d-flex">Poll Title</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="newPoll.title"
                  placeholder="Enter poll title"
                  required
                >
              </div>

              <!-- Poll Question -->
              <div class="mb-3">
                <label class="form-label text-start d-flex">Question</label>
                <textarea 
                  class="form-control" 
                  v-model="newPoll.questionText"
                  placeholder="Enter your question"
                  rows="3"
                  required
                ></textarea>
              </div>

              <!-- Poll Type -->
              <div class="mb-3">
                <label class="form-label text-start d-flex">Poll Type</label>
                <select class="form-select" v-model="newPoll.questionType" @change="resetOptions">
                  <option value="multiple_choice_single_selection">Multiple Choices; Respondents Select One</option>
                  <option value="multiple_choice_multi_selection">Multiple Choices; Respondents Select All That Apply</option>
                  <option value="rating_scale">Rating Scale; Respondents Select From 1-5</option>
                </select>
              </div>

              <!-- Options for Multiple Choice -->
              <div v-if="newPoll.questionType.includes('multiple_choice')" class="mb-3">
                <label class="form-label text-start d-flex">Options</label>
                <div 
                  v-for="(option, index) in newPoll.options" 
                  :key="index"
                  class="input-group mb-2"
                >
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="option.text"
                    :placeholder="`Option ${index + 1}`"
                    required
                  >
                  <button 
                    v-if="newPoll.options.length > 2"
                    type="button" 
                    class="btn btn-outline-danger" 
                    @click="removeOption(index)"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
                <button 
                  v-if="newPoll.options.length < 35"
                  type="button" 
                  class="btn btn-outline-secondary btn-sm" 
                  @click="addOption"
                >
                  <i class="bi bi-plus me-1"></i>Add Option
                </button>
              </div>

              <!-- Expiration Date -->
              <div class="mb-3">
                <label class="form-label text-start d-flex">Poll Closing Date (Optional)</label>
                <input 
                  type="datetime-local" 
                  class="form-control" 
                  v-model="newPoll.expiresAt"
                >
              </div>

              <!-- Visibility -->
              <div class="mb-3">
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    v-model="newPoll.isVisible"
                    id="pollVisible"
                  >
                  <label class="form-check-label" for="pollVisible">
                    Make poll visible to public
                  </label>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeCreateModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="createPoll">Create Poll</button>
          </div>
        </div>
      </div>
    </div>
    </div> <!-- Close poll-content-container -->
  </div> <!-- Close poll-card-container -->
</template>

<script>
export default {
  name: 'PollCard',
  props: {
    creatorId: {
      type: Number,
      required: true
    },
    creatorType: {
      type: String,
      required: true,
      validator: value => ['user', 'venue', 'producer'].includes(value)
    },
    currentUserId: {
      type: Number,
      default: null
    },
    currentUserType: {
      type: String,
      default: 'user',
      validator: value => ['user', 'venue', 'producer'].includes(value)
    },
    isCreator: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      // Poll data
      polls: [],
      pollResponses: [],
      currentPollIndex: 0,
      
      // Mobile collapse state
      isMobileCollapsed: true,
      
      // Detailed responses for creators
      detailedResponses: {}, // Store detailed responses by pollId
      showDetailedResponses: {}, // Track which polls have detailed responses visible
      loadingDetailedResponses: false,
      
      // User selections
      selectedSingleOption: null,
      selectedMultiOptions: [],
      selectedRating: null,
      userRating: null,
      
      // Modal state
      showCreateModal: false,
      showRandomWinnerModal: false,
      
      // Random winner state
      randomWinner: null,
      randomWinnerLoading: false,
      randomWinnerError: null,
      currentRandomPollId: null,
      
      // New poll form
      newPoll: {
        title: '',
        questionText: '',
        questionType: 'multiple_choice_single_selection',
        options: [
          { text: '' },
          { text: '' }
        ],
        expiresAt: null,
        isVisible: true
      }
    }
  },
  computed: {
    currentPoll() {
      return this.polls[this.currentPollIndex] || {};
    },
    
    visiblePolls() {
      if (this.isCreator) {
        return this.polls; // Creators can see all their polls
      }
      return this.polls.filter(poll => poll.isVisible);
    },

    // Get the current user's response for the current poll
    currentUserResponse() {
      if (!this.currentPoll.id || !this.currentUserId) return null;
      
      return this.pollResponses.find(response => 
        response.pollId === this.currentPoll.id && 
        response.respondentId === this.currentUserId
      );
    },

    // Check if current user has voted on current poll
    currentUserHasVoted() {
      return !!this.currentUserResponse;
    },

    // Check if current user can vote (only ordinary users who didn't create the poll)
    canUserVote() {
      // Must be logged in
      if (!this.currentUserId) return false;
      
      // Must be an ordinary user (not venue or producer)
      if (this.currentUserType !== 'user') return false;
      
      // Must not be the creator of the poll
      if (this.isCreator) return false;
      
      // Must not have already voted
      if (this.currentUserHasVoted) return false;
      
      return true;
    },

    // Check if user should see results (everyone except those who can vote)
    shouldShowResults() {
      return !this.canUserVote;
    }
  },
  methods: {
    // Navigation
    nextPoll() {
      if (this.currentPollIndex < this.polls.length - 1) {
        this.currentPollIndex++;
        this.resetSelections();
      }
    },
    
    previousPoll() {
      if (this.currentPollIndex > 0) {
        this.currentPollIndex--;
        this.resetSelections();
      }
    },
    
    resetSelections() {
      this.selectedSingleOption = null;
      this.selectedMultiOptions = [];
      this.selectedRating = null;
      this.userRating = null;
    },

    // Mobile collapse functionality
    toggleMobileCollapse() {
      this.isMobileCollapsed = !this.isMobileCollapsed;
    },

    // Manual SignUp Popup trigger method - emits event to parent
    triggerSignUpPopup() {
      this.$emit('trigger-signup-popup');
      console.log('🎪 PollCard: Emitting signup popup trigger event to parent');
    },
    
    // Single Choice Voting
    selectSingleOption(pollId, optionId) {
      this.selectedSingleOption = optionId;
    },
    
    submitSingleChoice(pollId) {
      if (this.selectedSingleOption) {
        this.submitVote(pollId, [this.selectedSingleOption], null);
      }
    },
    
    // Multi Choice Voting
    toggleMultiOption(optionId) {
      const index = this.selectedMultiOptions.indexOf(optionId);
      if (index > -1) {
        this.selectedMultiOptions.splice(index, 1);
      } else {
        this.selectedMultiOptions.push(optionId);
      }
    },
    
    submitMultiChoice(pollId) {
      if (this.selectedMultiOptions.length > 0) {
        this.submitVote(pollId, this.selectedMultiOptions, null);
      }
    },
    
    // Rating Scale Voting
    selectRating(pollId, rating) {
      this.selectedRating = rating;
      this.submitVote(pollId, null, rating);
    },
    
    // Submit Vote
    async submitVote(pollId, selectedOptionIds, ratingValue) {
      if (!this.currentUserId) {
        alert('Please log in to vote on polls.');
        return;
      }
      
      try {
        const voteData = {
          pollId,
          respondentId: this.currentUserId,
          selectedOptionIds,
          ratingValue
        };
        
        console.log('Submitting vote:', voteData);
        
        // Submit vote to backend endpoint
        const response = await fetch(`${process.env.VUE_APP_API_URL}/submitPoll/submitResponse`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(voteData)
        });
        
        if (response.ok) {
          const responseData = await response.json();
          
          if (responseData.code === 200) {
            // Reload poll responses to get the latest data including the new vote
            await this.loadPollResponses();
            
            // Reset selections
            this.resetSelections();
            
            console.log('Vote submitted successfully');
          } else {
            console.error('Failed to submit vote:', responseData.message);
            alert('Failed to submit vote. Please try again.');
          }
        } else {
          console.error('Failed to submit vote:', response.statusText);
          alert('Failed to submit vote. Please try again.');
        }
        
      } catch (error) {
        console.error('Error submitting vote:', error);
        
        // Fallback for development - add to local responses
        if (process.env.NODE_ENV === 'development') {
          console.log('Using local fallback for vote submission...');
          const response = {
            id: Date.now(), // Temporary ID
            pollId,
            respondentId: this.currentUserId,
            selectedOptionIds,
            ratingValue
          };
          
          this.pollResponses.push(response);
          this.resetSelections();
        } else {
          alert('Network error. Please check your connection and try again.');
        }
      }
    },
    
    // Check if user has answered
    hasAnswered(pollId) {
      return this.pollResponses.some(response => 
        response.pollId === pollId && response.respondentId === this.currentUserId
      );
    },
    
    // Results calculations
    getTotalVotes(pollId) {
      return this.pollResponses.filter(response => response.pollId === pollId).length;
    },
    
    getOptionPercentage(pollId, optionId) {
      const totalVotes = this.getTotalVotes(pollId);
      if (totalVotes === 0) return 0;
      
      const optionVotes = this.pollResponses.filter(response => 
        response.pollId === pollId && 
        response.selectedOptionIds && 
        response.selectedOptionIds.includes(optionId)
      ).length;
      
      return Math.round((optionVotes / totalVotes) * 100);
    },
    
    userVotedForOption(pollId, optionId) {
      const userResponse = this.pollResponses.find(response => 
        response.pollId === pollId && response.respondentId === this.currentUserId
      );
      
      return userResponse && 
             userResponse.selectedOptionIds && 
             userResponse.selectedOptionIds.includes(optionId);
    },
    
    getAverageRating(pollId) {
      const ratingResponses = this.pollResponses.filter(response => 
        response.pollId === pollId && response.ratingValue
      );
      
      if (ratingResponses.length === 0) return 0;
      
      const sum = ratingResponses.reduce((acc, response) => acc + response.ratingValue, 0);
      return (sum / ratingResponses.length).toFixed(1);
    },
    
    getRatingPercentage(pollId, rating) {
      const totalVotes = this.getTotalVotes(pollId);
      if (totalVotes === 0) return 0;
      
      const ratingVotes = this.pollResponses.filter(response => 
        response.pollId === pollId && response.ratingValue === rating
      ).length;
      
      return Math.round((ratingVotes / totalVotes) * 100);
    },
    
    getRatingCount(pollId, rating) {
      return this.pollResponses.filter(response => 
        response.pollId === pollId && response.ratingValue === rating
      ).length;
    },

    // Get text for user's selected options (for display purposes)
    getUserSelectedOptionText(selectedOptionIds) {
      if (!selectedOptionIds || !Array.isArray(selectedOptionIds) || selectedOptionIds.length === 0) {
        return 'No selection';
      }
      
      // For single selection, return the first (and only) option
      const optionId = selectedOptionIds[0];
      const option = this.currentPoll.options?.find(opt => opt.id === optionId);
      return option ? option.optionText : 'Unknown option';
    },

    getUserSelectedOptionsText(selectedOptionIds) {
      if (!selectedOptionIds || !Array.isArray(selectedOptionIds) || selectedOptionIds.length === 0) {
        return 'No selections';
      }
      
      // For multi-selection, return comma-separated list
      const selectedOptions = this.currentPoll.options?.filter(opt => 
        selectedOptionIds.includes(opt.id)
      ) || [];
      
      return selectedOptions.map(opt => opt.optionText).join(', ');
    },
    
    // Creator Controls
    async toggleVisibility(poll) {
      try {
        // Update poll visibility via backend endpoint
        const response = await fetch(`${process.env.VUE_APP_API_URL}/editPoll/updatePollVisibility/${poll.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ isVisible: !poll.isVisible })
        });
        
        if (response.ok) {
          const responseData = await response.json();
          if (responseData.code === 200) {
            poll.isVisible = !poll.isVisible;
            console.log('Visibility updated for poll:', poll.id, 'to:', poll.isVisible);
          } else {
            console.error('Failed to update poll visibility:', responseData.message);
            alert('Failed to update poll visibility: ' + responseData.message);
          }
        } else {
          console.error('Failed to update poll visibility:', response.statusText);
          alert('Failed to update poll visibility. Please try again.');
        }
        
      } catch (error) {
        console.error('Error updating poll visibility:', error);
        alert('Failed to update poll visibility. Please try again.');
      }
    },
    
    async deletePoll(pollId) {
      if (confirm('Are you sure you want to delete this poll? This action cannot be undone.')) {
        try {
          // Delete poll via backend endpoint
          const response = await fetch(`${process.env.VUE_APP_API_URL}/editPoll/deletePoll/${pollId}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            }
          });
          
          if (response.ok) {
            const responseData = await response.json();
            if (responseData.code === 200) {
              const index = this.polls.findIndex(poll => poll.id === pollId);
              if (index > -1) {
                this.polls.splice(index, 1);
                // Adjust current index if necessary
                if (this.currentPollIndex >= this.polls.length) {
                  this.currentPollIndex = Math.max(0, this.polls.length - 1);
                }
              }
              console.log('Poll deleted successfully:', pollId);
            } else {
              console.error('Failed to delete poll:', responseData.message);
              alert('Failed to delete poll: ' + responseData.message);
            }
          } else {
            console.error('Failed to delete poll:', response.statusText);
            alert('Failed to delete poll. Please try again.');
          }
          
        } catch (error) {
          console.error('Error deleting poll:', error);
          alert('Failed to delete poll. Please try again.');
        }
      }
    },
    
    // Random Winner Modal Management
    openRandomPickWinnerModal(pollId) {
      this.currentRandomPollId = pollId;
      this.showRandomWinnerModal = true;
      this.pickRandomWinner(pollId);
    },

    closeRandomWinnerModal() {
      this.showRandomWinnerModal = false;
      this.randomWinner = null;
      this.randomWinnerError = null;
      this.currentRandomPollId = null;
    },

    async pickRandomWinner(pollId) {
      this.randomWinnerLoading = true;
      this.randomWinner = null;
      this.randomWinnerError = null;

      try {
        // Add a minimum delay for the animation effect (1.5 seconds)
        const minDelay = new Promise(resolve => setTimeout(resolve, 1500));
        
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/getData/randomPickRespondentForOnePoll/${pollId}`
        );

        // Wait for minimum delay to complete
        await minDelay;

        if (response.ok) {
          const result = await response.json();
          
          if (result.code === 200 && result.data) {
            if (result.data.randomRespondent) {
              this.randomWinner = result.data.randomRespondent;
            } else {
              this.randomWinnerError = result.message || 'No responses found for this poll.';
            }
          } else {
            this.randomWinnerError = result.message || 'Failed to select a winner.';
          }
        } else {
          this.randomWinnerError = 'Failed to connect to the server.';
        }
      } catch (error) {
        console.error('Error picking random winner:', error);
        this.randomWinnerError = 'An error occurred while selecting a winner.';
      } finally {
        this.randomWinnerLoading = false;
      }
    },

    pickAnotherWinner() {
      if (this.currentRandomPollId) {
        this.pickRandomWinner(this.currentRandomPollId);
      }
    },

    // Modal Management
    closeCreateModal() {
      this.showCreateModal = false;
      this.resetNewPollForm();
    },
    
    resetNewPollForm() {
      this.newPoll = {
        title: '',
        questionText: '',
        questionType: 'multiple_choice_single_selection',
        options: [
          { text: '' },
          { text: '' }
        ],
        expiresAt: null,
        isVisible: true
      };
    },
    
    resetOptions() {
      this.newPoll.options = [
        { text: '' },
        { text: '' }
      ];
    },
    
    addOption() {
      if (this.newPoll.options.length < 35) {
        this.newPoll.options.push({ text: '' });
      }
    },
    
    removeOption(index) {
      if (this.newPoll.options.length > 2) {
        this.newPoll.options.splice(index, 1);
      }
    },
    
    async createPoll() {
      // Validate form
      if (!this.newPoll.title.trim() || !this.newPoll.questionText.trim()) {
        alert('Please fill in the title and question.');
        return;
      }
      
      if (this.newPoll.questionType.includes('multiple_choice')) {
        const validOptions = this.newPoll.options.filter(option => option.text.trim());
        if (validOptions.length < 2) {
          alert('Please provide at least 2 options.');
          return;
        }
      }
      
      try {
        const pollData = {
          creatorId: this.creatorId,
          creatorType: this.creatorType,
          title: this.newPoll.title.trim(),
          questionText: this.newPoll.questionText.trim(),
          questionType: this.newPoll.questionType,
          isVisible: this.newPoll.isVisible,
          expiresAt: this.newPoll.expiresAt || null,
          // orderIndex will be calculated by backend
          options: []
        };
        
        // Add options for multiple choice questions
        if (this.newPoll.questionType.includes('multiple_choice')) {
          pollData.options = this.newPoll.options
            .filter(option => option.text.trim())
            .map((option, index) => ({
              optionText: option.text.trim(),
              optionOrder: index
            }));
        }
        
        console.log('Creating poll:', pollData);
        
        // Submit poll to backend endpoint
        const response = await fetch(`${process.env.VUE_APP_API_URL}/editPoll/createPoll`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pollData)
        });
        
        if (response.ok) {
          const responseData = await response.json();
          if (responseData.code === 200) {
            // Reload polls to get the newly created poll
            await this.loadPolls();
            this.currentPollIndex = this.polls.length - 1;
            this.closeCreateModal();
            console.log('Poll created successfully:', responseData.data);
          } else {
            console.error('Failed to create poll:', responseData.message);
            alert('Failed to create poll: ' + responseData.message);
          }
        } else {
          console.error('Failed to create poll:', response.statusText);
          alert('Failed to create poll. Please try again.');
        }
        
      } catch (error) {
        console.error('Error creating poll:', error);
        
        // Fallback to mock data for development when backend is not available
        if (process.env.NODE_ENV === 'development') {
          console.log('Using local fallback for poll creation...');
          
          // Recreate the options data for the fallback
          let fallbackOptions = [];
          if (this.newPoll.questionType.includes('multiple_choice')) {
            fallbackOptions = this.newPoll.options
              .filter(option => option.text.trim())
              .map((option, index) => ({
                id: Date.now() + index, // Temporary ID
                pollId: Date.now(),
                optionText: option.text.trim(),
                optionOrder: index
              }));
          }
          
          // Calculate next orderIndex safely
          const maxOrderIndex = this.polls.length > 0 ? Math.max(...this.polls.map(p => p.orderIndex || 0)) : -1;
          const nextOrderIndex = maxOrderIndex + 1;
          
          const newPoll = {
            id: Date.now(), // Temporary ID
            creatorId: this.creatorId,
            creatorType: this.creatorType,
            title: this.newPoll.title.trim(),
            questionText: this.newPoll.questionText.trim(),
            questionType: this.newPoll.questionType,
            isActive: true,
            isVisible: this.newPoll.isVisible,
            expiresAt: this.newPoll.expiresAt || null,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            orderIndex: nextOrderIndex,
            options: fallbackOptions
          };
          
          this.polls.push(newPoll);
          this.currentPollIndex = this.polls.length - 1;
          this.closeCreateModal();
        } else {
          alert('Failed to create poll. Please check your connection and try again.');
        }
      }
    },
    
    // Utility
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },

    formatRelativeTime(dateString) {
      if (!dateString) return '';
      
      const targetDate = new Date(dateString);
      const now = new Date();
      const diffMs = targetDate.getTime() - now.getTime();
      
      // If the date is in the past, show "Expired"
      if (diffMs < 0) {
        const pastDiffMs = Math.abs(diffMs);
        const pastMinutes = Math.floor(pastDiffMs / (1000 * 60));
        const pastHours = Math.floor(pastDiffMs / (1000 * 60 * 60));
        const pastDays = Math.floor(pastDiffMs / (1000 * 60 * 60 * 24));
        
        if (pastDays > 0) {
          return `Expired ${pastDays} day${pastDays > 1 ? 's' : ''} ago`;
        } else if (pastHours > 0) {
          return `Expired ${pastHours} hour${pastHours > 1 ? 's' : ''} ago`;
        } else if (pastMinutes > 0) {
          return `Expired ${pastMinutes} minute${pastMinutes > 1 ? 's' : ''} ago`;
        } else {
          return 'Expired';
        }
      }
      
      // Calculate time remaining
      const minutes = Math.floor(diffMs / (1000 * 60));
      const hours = Math.floor(diffMs / (1000 * 60 * 60));
      const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      const weeks = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 7));
      const months = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 30));
      
      if (months > 0) {
        return `Expires in ${months} month${months > 1 ? 's' : ''}`;
      } else if (weeks > 0) {
        return `Expires in ${weeks} week${weeks > 1 ? 's' : ''}`;
      } else if (days > 0) {
        return `Expires in ${days} day${days > 1 ? 's' : ''}`;
      } else if (hours > 0) {
        return `Expires in ${hours} hour${hours > 1 ? 's' : ''}`;
      } else if (minutes > 0) {
        return `Expires in ${minutes} minute${minutes > 1 ? 's' : ''}`;
      } else {
        return 'Expires very soon';
      }
    },

    getExpirationBadgeClass(dateString) {
      if (!dateString) return 'bg-info';
      
      const targetDate = new Date(dateString);
      const now = new Date();
      const diffMs = targetDate.getTime() - now.getTime();
      
      // If expired, show red
      if (diffMs < 0) {
        return 'bg-danger';
      }
      
      const hours = Math.floor(diffMs / (1000 * 60 * 60));
      const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      
      // If expiring within 1 hour, show red
      if (hours < 1) {
        return 'bg-danger';
      }
      // If expiring within 24 hours, show orange/warning
      else if (days < 1) {
        return 'bg-warning';
      }
      // Otherwise, show blue/info
      else {
        return 'bg-info';
      }
    },

    formatResponseDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },

    // Detailed Responses Management
    async toggleDetailedResponses(pollId) {
      // If already showing, just hide
      if (this.showDetailedResponses[pollId]) {
        this.showDetailedResponses[pollId] = false;
        return;
      }

      // If not loaded yet, load the detailed responses
      if (!this.detailedResponses[pollId]) {
        await this.loadDetailedResponses(pollId);
      }

      // Toggle visibility
      this.showDetailedResponses[pollId] = !this.showDetailedResponses[pollId];
    },

    async loadDetailedResponses(pollId) {
      this.loadingDetailedResponses = true;
      
      try {
        // Fetch detailed responses for this specific poll
        const response = await fetch(`${process.env.VUE_APP_API_URL}/getData/getPollResponses/${this.creatorId}/${this.creatorType}`);
        
        if (response.ok) {
          const responseData = await response.json();
          
          if (responseData.code === 200) {
            // Find the specific poll's responses
            const pollData = responseData.data.find(poll => poll.pollId === pollId);
            
            if (pollData && pollData.responses) {
              // Store the detailed responses for this poll
              this.detailedResponses[pollId] = pollData.responses;
              console.log('Loaded detailed responses for poll', pollId, ':', pollData.responses);
            } else {
              // No responses found for this poll
              this.detailedResponses[pollId] = [];
            }
          } else {
            console.error('Error loading detailed responses:', responseData.message);
            this.detailedResponses[pollId] = [];
          }
        } else {
          console.error('Failed to load detailed responses:', response.statusText);
          this.detailedResponses[pollId] = [];
        }
        
      } catch (error) {
        console.error('Error loading detailed responses:', error);
        this.detailedResponses[pollId] = [];
      } finally {
        this.loadingDetailedResponses = false;
      }
    },

    // Helper method to get option text by ID
    getOptionTextById(optionId) {
      if (!this.currentPoll.options) return 'Unknown option';
      
      const option = this.currentPoll.options.find(opt => opt.id === optionId);
      return option ? option.optionText : `Option ${optionId}`;
    },
    
    // Load data from backend API
    async loadPolls() {
      try {
        // Fetch polls for this creator using the correct backend endpoint
        const pollsResponse = await fetch(`${process.env.VUE_APP_API_URL}/getData/getPollsByCreator/${this.creatorId}/${this.creatorType}`);
        
        if (pollsResponse.ok) {
          const pollsData = await pollsResponse.json();
          
          if (pollsData.code === 200) {
            // Process polls and their options
            this.polls = pollsData.data.map(poll => ({
              ...poll,
              options: poll.options || [] // Ensure options array exists
            }));
            
            // Filter visible polls for non-creators
            if (!this.isCreator) {
              this.polls = this.polls.filter(poll => poll.isVisible);
            }
            
            console.log('Loaded polls:', this.polls);
          } else {
            console.error('Error loading polls:', pollsData.message);
            // Use mock data as fallback when API returns error
            console.log('Using mock data as fallback...');
            this.loadMockData();
            return;
          }
        } else {
          console.error('Failed to load polls:', pollsResponse.statusText);
          // Use mock data as fallback when API call fails
          console.log('Using mock data as fallback...');
          this.loadMockData();
          return;
        }
        
        // Load poll responses
        await this.loadPollResponses();
        
      } catch (error) {
        console.error('Error loading polls:', error);
        
        // Fallback to mock data for any error (network issues, API not available, etc.)
        console.log('Using mock data as fallback...');
        this.loadMockData();
      }
    },

    // Load poll responses from backend API
    async loadPollResponses() {
      try {
        // Fetch poll responses for this creator using the correct backend endpoint
        const responsesResponse = await fetch(`${process.env.VUE_APP_API_URL}/getData/getPollResponses/${this.creatorId}/${this.creatorType}`);
        
        if (responsesResponse.ok) {
          const responsesData = await responsesResponse.json();
          
          if (responsesData.code === 200) {
            // Process the raw response data into the format the component expects
            this.pollResponses = this.processRawResponseData(responsesData.data);
            
            console.log('Loaded poll responses:', this.pollResponses);
            console.log('Raw response data:', responsesData.data);
          } else {
            console.error('Error loading poll responses:', responsesData.message);
            // Use empty responses array when API returns error
            this.pollResponses = [];
          }
        } else {
          console.error('Failed to load poll responses:', responsesResponse.statusText);
          // Use empty responses array when API call fails
          this.pollResponses = [];
        }
        
      } catch (error) {
        console.error('Error loading poll responses:', error);
        // Use empty responses array for any error
        this.pollResponses = [];
      }
    },

    // Process raw response data from backend into component-expected format
    processRawResponseData(rawData) {
      const processedResponses = [];
      
      // Iterate through each poll's response data
      rawData.forEach(pollData => {
        const { pollId, responses } = pollData;
        
        // Process each individual response
        responses.forEach(response => {
          processedResponses.push({
            id: response.responseId,
            pollId: pollId,
            respondentId: response.respondentId,
            selectedOptionIds: response.selectedOptionIds,
            ratingValue: response.ratingValue,
            // Additional data for potential future use
            respondentUsername: response.respondentUsername,
            respondentDisplayName: response.respondentDisplayName
          });
        });
      });
      
      return processedResponses;
    },

    // Refresh poll data (useful for real-time updates)
    async refreshPollData() {
      await this.loadPollResponses();
    },

    // Debug helper method
    debugCurrentState() {
      console.log('=== POLL DEBUG INFO ===');
      console.log('Current Poll:', this.currentPoll);
      console.log('Current User ID:', this.currentUserId, '(type:', typeof this.currentUserId, ')');
      console.log('Current User Type:', this.currentUserType);
      console.log('Is Creator:', this.isCreator);
      console.log('Can User Vote:', this.canUserVote);
      console.log('Should Show Results:', this.shouldShowResults);
      console.log('All Poll Responses:', this.pollResponses);
      
      // Debug respondent IDs and types
      if (this.pollResponses.length > 0) {
        console.log('Sample respondent IDs:');
        this.pollResponses.slice(0, 3).forEach(response => {
          console.log('- Respondent ID:', response.respondentId, '(type:', typeof response.respondentId, ')');
        });
      }
      
      console.log('Current User Response:', this.currentUserResponse);
      console.log('User Has Voted:', this.currentUserHasVoted);
      
      if (this.currentUserResponse) {
        console.log('User Previous Selection:');
        if (this.currentUserResponse.selectedOptionIds) {
          console.log('- Selected Options:', this.getUserSelectedOptionsText(this.currentUserResponse.selectedOptionIds));
        }
        if (this.currentUserResponse.ratingValue) {
          console.log('- Rating:', this.currentUserResponse.ratingValue);
        }
      }
      
      console.log('======================');
    },
    
    // Mock data for development/testing
    loadMockData() {
      this.polls = [
        {
          id: 1,
          creatorId: this.creatorId,
          creatorType: this.creatorType,
          title: "What's your favorite drink type?",
          questionText: "Help us understand your preferences better!",
          questionType: 'multiple_choice_single_selection',
          isActive: true,
          isVisible: true,
          expiresAt: null,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          orderIndex: 0,
          options: [
            { id: 1, pollId: 1, optionText: 'Wine', optionOrder: 0 },
            { id: 2, pollId: 1, optionText: 'Beer', optionOrder: 1 },
            { id: 3, pollId: 1, optionText: 'Spirits', optionOrder: 2 },
            { id: 4, pollId: 1, optionText: 'Cocktails', optionOrder: 3 }
          ]
        },
        {
          id: 2,
          creatorId: this.creatorId,
          creatorType: this.creatorType,
          title: "Which activities would you like to see?",
          questionText: "Select all that apply for future events!",
          questionType: 'multiple_choice_multi_selection',
          isActive: true,
          isVisible: true,
          expiresAt: null,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          orderIndex: 1,
          options: [
            { id: 5, pollId: 2, optionText: 'Live Music', optionOrder: 0 },
            { id: 6, pollId: 2, optionText: 'Food Pairing', optionOrder: 1 },
            { id: 7, pollId: 2, optionText: 'Masterclasses', optionOrder: 2 },
            { id: 8, pollId: 2, optionText: 'Meet & Greet', optionOrder: 3 }
          ]
        },
        {
          id: 3,
          creatorId: this.creatorId,
          creatorType: this.creatorType,
          title: "Rate our service quality",
          questionText: "How satisfied are you with our overall service?",
          questionType: 'rating_scale',
          isActive: true,
          isVisible: true,
          expiresAt: null,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          orderIndex: 2,
          options: [] // No options needed for rating scale
        }
      ];
      
      // Mock responses for demonstration - more realistic data
      this.pollResponses = [
        { id: 1, pollId: 1, respondentId: 101, selectedOptionIds: [1], ratingValue: null },
        { id: 2, pollId: 1, respondentId: 102, selectedOptionIds: [2], ratingValue: null },
        { id: 3, pollId: 1, respondentId: 103, selectedOptionIds: [1], ratingValue: null },
        { id: 4, pollId: 1, respondentId: 104, selectedOptionIds: [3], ratingValue: null },
        { id: 5, pollId: 1, respondentId: 105, selectedOptionIds: [1], ratingValue: null },
        { id: 6, pollId: 2, respondentId: 101, selectedOptionIds: [5, 6], ratingValue: null },
        { id: 7, pollId: 2, respondentId: 102, selectedOptionIds: [6, 7, 8], ratingValue: null },
        { id: 8, pollId: 2, respondentId: 103, selectedOptionIds: [5, 7], ratingValue: null },
        { id: 9, pollId: 3, respondentId: 102, selectedOptionIds: null, ratingValue: 4 },
        { id: 10, pollId: 3, respondentId: 103, selectedOptionIds: null, ratingValue: 5 },
        { id: 11, pollId: 3, respondentId: 104, selectedOptionIds: null, ratingValue: 3 },
        { id: 12, pollId: 3, respondentId: 105, selectedOptionIds: null, ratingValue: 4 }
      ];
    }
  },

  watch: {
    // Debug watcher for development
    pollResponses: {
      handler() {
        if (process.env.NODE_ENV === 'development') {
          console.log('Poll responses updated, current state:');
          this.debugCurrentState();
        }
      },
      deep: true
    },

    currentPollIndex() {
      if (process.env.NODE_ENV === 'development') {
        console.log('Poll changed, current state:');
        this.debugCurrentState();
      }
    }
  },
  
  mounted() {
    this.loadPolls();
  }
}
</script>

<style scoped>
.poll-card-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border-color: #F2994A;
  border-width: 2px;
  border-style: solid;
}

/* Collapse Header - Visible on both desktop and mobile */
.mobile-collapse-header {
  display: block;
  padding: 15px 20px;
  background-color: #ffe9b6;
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.mobile-collapse-header:hover {
  background-color: #fbf1d8;
}


.mobile-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mobile-header-info {
  flex: 1;
}

.mobile-poll-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  display: block;
  width: 100%;
}

.mobile-poll-title-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mobile-poll-text {
  color: #2c3e50;
  flex: 1;
}

.mobile-poll-count {
  font-size: 0.875rem;
  color: #6c757d;
}

.mobile-collapse-icon {
  display: flex;
  align-items: center;
  color: #6c757d;
}

/* Poll Content Container */
.poll-content-container {
  transition: all 0.3s ease;
  overflow: hidden;
}

/* Desktop and Mobile: Apply collapsed state */
.poll-content-container.collapsed {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}

.poll-content-container:not(.collapsed) {
  max-height: 3000px;
  opacity: 1;
}

.poll-carousel {
  position: relative;
  display: flex;
  align-items: center;
  min-height: 400px;
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #dee2e6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.carousel-arrow:hover:not(:disabled) {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.carousel-arrow:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carousel-arrow-left {
  left: 10px;
}

.carousel-arrow-right {
  right: 10px;
}

/* Header Navigation Arrows - Always visible at the top */
.header-nav-arrow {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #dee2e6;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  min-width: 36px;
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.header-nav-arrow:hover:not(:disabled) {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transform: scale(1.05);
}

.header-nav-arrow:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.header-nav-arrow i {
  font-size: 1.2rem;
  color: #495057;
}

.header-nav-arrow-left {
  margin-right: 12px;
}

.header-nav-arrow-right {
  margin-left: 12px;
}

.poll-card {
  flex: 1;
  padding: 20px;
  margin: 0 60px;
}

.poll-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.poll-title-section {
  flex: 1;
  min-width: 0;
}

.poll-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #2c3e50;
  display: block;
  width: 100%;
}

.poll-title-content {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.poll-icon {
  color: #007bff;
  font-size: 1.1rem;
  margin-right: 8px;
}

.poll-label {
  color: #007bff;
  font-weight: 600;
}

.poll-title-text {
  color: #2c3e50;
  flex: 1;
}

.poll-question {
  font-weight:bold;
  margin-bottom: 10px;
  line-height: 1.5;
}

.poll-controls {
  display: flex;
  gap: 5px;
}

.poll-status {
  margin-bottom: 15px;
}

.poll-status .badge {
  font-size: 0.75rem;
}

/* User Status Message */
.user-status-message {
  border-radius: 8px;
}

.user-status-message .alert {
  margin-bottom: 0;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
}

/* Voting Styles */
.poll-option {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 8px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.poll-option:hover {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.poll-option.selected {
  border-color: #007bff;
  background-color: #e7f3ff;
}

.option-radio,
.option-checkbox {
  margin-right: 12px;
}

.option-text {
  flex: 1;
  font-weight: 500;
}

/* Rating Scale */
.rating-scale {
  text-align: center;
}

.rating-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  font-size: 0.875rem;
  color: #6c757d;
}

.rating-options {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.rating-option {
  cursor: pointer;
}

.rating-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.2s ease;
}

.rating-option:hover .rating-circle {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.rating-option.selected .rating-circle {
  border-color: #007bff;
  background-color: #007bff;
  color: white;
}

/* Results Styles */
.poll-results {
  margin-top: 20px;
}

.user-vote-indicator {
  border-radius: 8px;
}

.user-vote-indicator .alert {
  margin-bottom: 0;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
}

.result-option {
  margin-bottom: 12px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.percentage {
  font-weight: 600;
  color: #007bff;
}

.progress {
  height: 25px;
  background-color: #e9ecef;
  border-radius: 12px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.progress-bar.user-voted {
  background-color: #28a745;
}

.total-votes {
  text-align: center;
  margin-top: 15px;
  color: #6c757d;
  font-size: 0.9rem;
}

/* Rating Results */
.rating-results {
  text-align: center;
}

.rating-display {
  margin-bottom: 20px;
}

.rating-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #007bff;
}

.rating-scale-text {
  font-size: 1.2rem;
  color: #6c757d;
}

.rating-breakdown {
  max-width: 300px;
  margin: 0 auto;
}

.rating-bar {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 10px;
}

.rating-label {
  width: 20px;
  text-align: center;
  font-weight: 500;
}

.rating-bar .progress {
  flex: 1;
  height: 20px;
}

.rating-count {
  width: 30px;
  text-align: center;
  font-size: 0.875rem;
  color: #6c757d;
}

/* Navigation Info */
.poll-navigation-info {
  text-align: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e9ecef;
}

.poll-counter {
  color: #6c757d;
  font-size: 0.875rem;
}

/* Create Poll Section */
.create-poll-section {
  padding: 20px;
  border-top: 1px solid #e9ecef;
}

.create-poll-section .btn {
  line-height: 1.4;
  padding: 15px 20px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  /* Mobile-specific adjustments */
  .poll-card {
    margin: 0 50px;
    padding: 15px;
  }
  
  .carousel-arrow {
    width: 35px;
    height: 35px;
  }
  
  .carousel-arrow-left {
    left: 5px;
  }
  
  .carousel-arrow-right {
    right: 5px;
  }

  .header-nav-arrow {
    width: 32px;
    height: 32px;
    min-width: 32px;
    min-height: 32px;
  }

  .header-nav-arrow i {
    font-size: 1rem;
  }

  .header-nav-arrow-left {
    margin-right: 8px;
  }

  .header-nav-arrow-right {
    margin-left: 8px;
  }
  
  .poll-header {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
  }

  .poll-title-section {
    flex-basis: 100%;
    order: 2;
  }
  
  .poll-controls {
    align-self: flex-end;
  }
  
  .rating-options {
    gap: 10px;
  }
  
  .rating-circle {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .rating-breakdown {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .poll-card {
    margin: 0 0px;
    padding: 12px;
  }
  
  .poll-title {
    display:none;
  }

  .header-nav-arrow {
    width: 28px;
    height: 28px;
    min-width: 28px;
    min-height: 28px;
  }

  .header-nav-arrow i {
    font-size: 0.9rem;
  }

  .header-nav-arrow-left {
    margin-right: 6px;
  }

  .header-nav-arrow-right {
    margin-left: 6px;
  }
  
  .poll-option {
    padding: 10px 12px;
  }
  
  .rating-options {
    gap: 8px;
  }
  
  .rating-circle {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
}

/* Creator Detailed Responses Section */
.creator-responses-section {
  border-top: 1px solid #e9ecef;
  padding-top: 15px;
}

.detailed-responses-header .btn {
  font-size: 0.875rem;
  border-radius: 6px;
}

.detailed-responses-content {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #e9ecef;
}

.responses-title {
  color: #495057;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 15px;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 8px;
}

.response-item {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 12px 15px;
  margin-bottom: 12px;
  transition: all 0.2s ease;
}

.response-item:hover {
  border-color: #007bff;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.1);
}

.response-item:last-child {
  margin-bottom: 0;
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.respondent-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.respondent-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.respondent-username {
  color: #6c757d;
  font-size: 0.8rem;
}

.response-timestamp {
  color: #6c757d;
  font-size: 0.75rem;
  text-align: right;
}

.response-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.response-label {
  font-weight: 500;
  color: #495057;
  font-size: 0.875rem;
}

.response-value {
  color: #007bff;
  font-weight: 600;
  font-size: 0.875rem;
}

.rating-response {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-stars {
  display: inline-flex;
  gap: 2px;
}

.rating-stars i {
  font-size: 0.8rem;
}

.multi-selection-response {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.multi-selection-response .badge {
  font-size: 0.75rem;
  padding: 4px 8px;
}

.no-responses {
  text-align: center;
  color: #6c757d;
}

.loading-responses {
  color: #6c757d;
}

/* Mobile responsive for detailed responses */
@media (max-width: 768px) {
  .response-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .response-timestamp {
    text-align: left;
    font-size: 0.7rem;
  }
  
  .response-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .rating-stars i {
    font-size: 0.75rem;
  }
}

@media (max-width: 576px) {
  .detailed-responses-content {
    padding: 12px;
  }
  
  .response-item {
    padding: 10px 12px;
  }
  
  .respondent-name {
    font-size: 0.85rem;
  }
  
  .respondent-username {
    font-size: 0.75rem;
  }
  
  .multi-selection-response .badge {
    font-size: 0.7rem;
    padding: 3px 6px;
  }
}

/* User Rating Display for non-creators */
.user-rating-display {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 15px;
}

.rating-label-simple {
  font-size: 0.95rem;
  color: #6c757d;
  font-weight: 500;
}

.user-rating-stars {
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-rating-stars i {
  transition: color 0.2s ease;
}

/* Random Winner Modal Styles */
.winner-loading-container {
  text-align: center;
  padding: 40px 20px;
}

.lottery-animation {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto;
}

.lottery-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border: 8px solid #f3f3f3;
  border-top: 8px solid #28a745;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

.lottery-balls {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
}

.lottery-ball {
  position: absolute;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  border-radius: 50%;
  animation: bounce 0.6s ease-in-out infinite;
}

.lottery-ball:nth-child(1) {
  top: 10px;
  left: 30px;
  animation-delay: 0s;
}

.lottery-ball:nth-child(2) {
  top: 30px;
  left: 50px;
  animation-delay: 0.2s;
}

.lottery-ball:nth-child(3) {
  top: 50px;
  left: 30px;
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.loading-text {
  color: #6c757d;
  font-size: 1.1rem;
  font-weight: 500;
}

.winner-display {
  text-align: center;
  padding: 20px;
}

.winner-announcement {
  position: relative;
}

.confetti {
  font-size: 3rem;
  animation: confetti-fall 0.8s ease-out;
}

@keyframes confetti-fall {
  0% {
    transform: translateY(-100px) scale(0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.winner-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #28a745;
  margin: 15px 0;
}

.winner-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  padding: 30px;
  margin: 20px 0;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  animation: slide-up 0.5s ease-out;
}

@keyframes slide-up {
  0% {
    transform: translateY(30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.winner-icon {
  font-size: 4rem;
  color: white;
  margin-bottom: 15px;
}

.winner-info {
  color: white;
}

.winner-name {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
  color: white;
}

.winner-username {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
}

.winner-response {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  text-align: left;
}

.response-header {
  font-weight: 600;
  color: #495057;
  margin-bottom: 15px;
  text-align: center;
}

.response-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.response-option {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background: white;
  border-radius: 8px;
  border: 2px solid #28a745;
  font-weight: 500;
  color: #2c3e50;
}

.rating-display-winner {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
}

.rating-display-winner i {
  font-size: 1.8rem;
}

.no-winner-state {
  text-align: center;
  padding: 40px 20px;
}

.no-winner-icon {
  font-size: 4rem;
  color: #6c757d;
  margin-bottom: 20px;
}

.no-winner-text {
  font-size: 1.1rem;
  color: #6c757d;
}

/* Mobile responsive for winner modal */
@media (max-width: 576px) {
  .winner-card {
    padding: 20px;
  }

  .winner-name {
    font-size: 1.2rem;
  }

  .winner-icon {
    font-size: 3rem;
  }

  .lottery-animation {
    width: 120px;
    height: 120px;
  }

  .lottery-spinner {
    width: 100px;
    height: 100px;
  }
}
</style>