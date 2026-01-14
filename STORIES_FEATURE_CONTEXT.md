# Stories Feature - Next Chat Context Prompt

## Overview and requirements
I'm working on the **DrinkX** platform - a drink review application. I've been implementing a **Stories feature** - a long-form content publishing system similar to Medium/Substack where users can publish articles about drinks.

The Stories feature allows users to publish long-form articles about drinks. It has two main organizational structures:
- **Topics**: Community categories anyone can write to (like subreddits)
- **Newsletters**: Personal publishing channels where only the creator can post (like Substack)

Stories can be linked to drinks in the database, display rich text content with images, and support community engagement through likes and comments.

## What Has Been Implemented (Placeholder Files with TODOs)

### Backend File Created:
- **`/backend/scripts/stories.py`** (~992 lines)
  - All endpoint stubs returning 501 Not Implemented
  - Helper functions for validation, name normalization
  - Topics endpoints (6): createTopic, getTopics, getTopicswSearch, getSpecificTopicInfo, subscribeTopic, unsubscribeTopic, getTopicStories
  - Newsletters endpoints (7): createNewsletter, getNewsletters, getNewsletterswSearch, getSpecificNewsletterInfo, getNewsletterStories, getUserNewsletters, subscribeNewsletter, unsubscribeNewsletter
  - Stories endpoints (7): createStory, getStory, editStory, deleteStory, getUserStories, likeStory, unlikeStory
  - Comments endpoints (5): createStoryComment, getStoryComments, likeStoryComment, dislikeStoryComment, deleteStoryComment
  - Blueprint auto-registered via `app.py` dynamic registration

### Backend Endpoints Implemented so far `/backend/scripts/stories.py`:

| Endpoint | Method | Lines | Purpose |
|----------|--------|-------|---------|
| `/createTopic` | POST | ~170-280 | Admin-only topic creation with S3 image upload, uniqueness check using `normalize_name_for_uniqueness()` |
| `/getTopics/<offset>` | GET | ~320-450 | Paginated topics (12/page) with computed `subscriberCount`/`storyCount`, `previewStories`, creator info |
| `/getTopicswSearch/<offset>/<search>` | GET | ~480-580 | Search by name/description using ILIKE |
| `/getSpecificTopicInfo/<topicID>` | GET | ~600-680 | Full topic details with `isSubscribed` flag (accepts `userID`/`userType` query params) |
| `/subscribeTopic` | POST | ~700-770 | Instant subscription - inserts into `topicSubscribers` |
| `/unsubscribeTopic` | DELETE | ~785-835 | Delete subscription from `topicSubscribers` |
| `/getTopicStories/<topicID>/<offset>` | GET | ~850-955 | Paginated published stories with creator info, like/comment counts |

### Key Backend Patterns Used:
- **Connection pooling**: `db_manager.get_cursor()` context manager
- **Uniqueness check**: `normalize_name_for_uniqueness()` imported from assembly module
- **Image upload**: `s3Images.uploadBase64ImageToS3(base64_data, folder='topics')`
- **Computed counts**: On-the-fly via subqueries (not denormalized columns)
- **Preview stories**: `get_story_preview_photos()` helper function


### Frontend Router Created:
- **`/frontend/src/router/modules/story.js`**
  - Routes with webpack chunking for Stories feature
  - Routes: browseStoryTopics, createTopic, specificStoryTopic, browseStoryNewsletters, createNewsletter, specificStoryNewsletter, specificStory

### Frontend Router Updates:
- **`/frontend/src/router/index.js`** - Added `import story` and `...story` in routes array
- **`/frontend/src/router/modules/profile.js`** - Added userStories route

### Frontend Component Updates:
- **`/frontend/src/components/UserProfileNavbar.vue`** - Added Stories link in navigation

### Frontend Views Created (all with placeholder TODO comments):
1. **`/frontend/src/views/Users/UserStories.vue`** (~450 lines)
   - User's profile page showing their stories
   - Create Story modal structure with topic/newsletter selectors
   - My Newsletters modal
   - Route: `/profile/user/:userID/:username/stories`

2. **`/frontend/src/views/BrowseStoryTopics.vue`** (~350 lines)
   - Browse all topics with Pinterest-style cards
   - Search, sort by recent/alphabetical
   - Route: `/stories/topics`

3. **`/frontend/src/views/SpecificStoryTopic.vue`** (~450 lines)
   - Hero banner with topic info
   - Subscribe/unsubscribe buttons
   - Stories feed with like/comment/share
   - Create story button (any logged-in user)
   - Route: `/stories/topics/:topicId/:topicName`

4. **`/frontend/src/views/BrowseStoryNewsletters.vue`** (~350 lines)
   - Browse all newsletters with cards
   - Search, sort by recent/alphabetical/subscribers
   - Route: `/stories/newsletters`

5. **`/frontend/src/views/SpecificStoryNewsletter.vue`** (~500 lines)
   - Hero banner with newsletter info
   - Subscribe button (in-app only for MVP)
   - Stories feed
   - Create story button (owner only)
   - Route: `/stories/newsletters/:newsletterId/:newsletterName`

6. **`/frontend/src/views/SpecificStory.vue`** (~550 lines)
   - Full story detail page
   - Rich text content display
   - Comments with likes/dislikes
   - Related drinks sidebar
   - Author info card
   - Share buttons
   - Route: `/stories/:storyId/:storyTitle`

7. **`/frontend/src/views/CreateTopic.vue`** (~400 lines)
   - Topic creation form
   - Name validation with uniqueness check
   - Drink type multi-select
   - Banner image upload
   - Live preview
   - Route: `/stories/topics/create`

8. **`/frontend/src/views/CreateNewsletter.vue`** (~450 lines)
   - Newsletter creation form
   - Name validation with uniqueness check
   - Optional topic association
   - Drink type multi-select
   - Cover image upload
   - Live preview
   - Route: `/stories/newsletters/create`


### Frontend Files Connected to Backend:

#### 1. `/frontend/src/views/BrowseStoryTopics.vue` (COMPLETE)
- Admin-only "Create Topic" button using `isAdmin` from localStorage
- Debounced search (300ms) via `searchTimeout`
- API calls: `getTopics/<offset>` and `getTopicswSearch/<offset>/<search>`
- Client-side sorting: `applySorting()` method (Newest, Alphabetical)
- Pagination with "Load More"

#### 2. `/frontend/src/views/CreateTopic.vue` (COMPLETE)
- Admin check with redirect for non-admins on mount
- Fetches drink types from `/getData/getDrinkTypes` (like CreateAssembly)
- Pill-style drink type selector with `toggleDrinkType()`
- Validation: 4-255 chars, emojis allowed (frontend only)
- Image upload: FileReader → base64 → sent to backend
- Submits to `/stories/createTopic`
- Handles duplicate name error (400 response)

#### 3. `/frontend/src/views/SpecificStoryTopic.vue` (COMPLETE)
- Loads topic info via `getSpecificTopicInfo/<topicID>?userID=X&userType=Y`
- `isSubscribed` flag displayed in UI
- Subscribe button calls `/stories/subscribeTopic` (POST)
- Unsubscribe button calls `/stories/unsubscribeTopic` (DELETE)
- Loads stories via `getTopicStories/<topicID>/<offset>`
- Client-side sorting (Newest, Most Liked)
- `transformStories()` method maps API response to template format
- "Create Story" navigates to `/stories/my-stories?createNew=true&topicID=X&topicName=Y`
- Back navigation uses `$router.back()`
- 404 handling redirects to `/stories/topics`



## Database Schema (Already in Production)
The database tables already exist in `/database/postgresql/final/01-postgresql_data3.sql` (lines 2111-2250):
- `topics` - Story topics/categories
- `topicSubscribers` - User subscriptions to topics
- `newsletters` - User-owned newsletters
- `newsletterPatrons` - Newsletter subscribers
- `stories` - Story content
- `storyPatrons` - Story-specific patron access (future)
- `storiesLikes` - Story likes
- `storyComments` - Comments on stories
- `storyCommentsLikes` - Comment likes
- `storyCommentsDislikes` - Comment dislikes
- `storyHashtags` - Story hashtag associations
- `hashtags` - Hashtag definitions

## Key Design Decisions Made:
1. **URL Hierarchy**: `/stories/topics/:id/:slug` and `/stories/newsletters/:id/:slug`
2. **Stories without newsletters**: Stories CAN exist without a newsletter (contrary to initial doc)
3. **Duplicate checking**: Global case-insensitive (with emoji stripped) for topic/newsletter names
4. **Likes system**: Likes only for stories; Likes AND dislikes for comments
5. **Paywall**: All newsletters treated as "free" for MVP
6. **Hashtags**: Managed separately with # prefix display
7. **Email delivery**: TODO for future - subscription is in-app only for MVP

## Reference Files (Model After These):
- Backend: `/backend/scripts/assembly.py` - Similar Blueprint structure
- Frontend Browse: `/frontend/src/views/BrowseAssemblies.vue`
- Frontend Detail: `/frontend/src/views/SpecificAssembly.vue`
- Frontend Item Detail: `/frontend/src/views/SpecificAssemblyPost.vue`
- Frontend Create: `/frontend/src/views/CreateAssembly.vue`

## Further Development Schedule
We are working **full-stack on a concept-by-concept basis**:
1. ✅ **Topics** (Admin creation) - `BrowseStoryTopics.vue`, `CreateTopic.vue`, `SpecificStoryTopic.vue`
2. ⏳ **Newsletters** (Individual creators) - `BrowseStoryNewsletters.vue`, `CreateNewsletter.vue`, `SpecificStoryNewsletter.vue`
3. ⏳ **Individual Stories** - `UserStories.vue`, `SpecificStory.vue`
4. ⏳ **Comments & Interactions** - Like/dislike, comments system

## Design Decisions Made for Topics (Carry Forward):

1. **Admin-only topic creation**: Checked via `users.isAdmin` column / `88B_isAdmin` localStorage
2. **Validation**: 4-255 characters, emojis allowed, frontend-only validation, backend checks uniqueness
3. **Drink types**: Fetched from `/getData/getDrinkTypes` API, stored as TEXT[] array
4. **Sorting**: Client-side only (no server sort parameter)
5. **Counts**: Computed on-the-fly with subqueries (not denormalized)
6. **Subscribe/Unsubscribe**: Instant, no approval needed, no notifications (for now)
7. **Story creation from topic**: Navigate to UserStories.vue with query params to pre-select topic


## What Remains To Be Implemented

### Phase 2: Newsletters (Next Priority)
**Files to implement:**
- `/frontend/src/views/BrowseStoryNewsletters.vue`
- `/frontend/src/views/CreateNewsletter.vue`
- `/frontend/src/views/SpecificStoryNewsletter.vue`

**Backend endpoints to implement in `/backend/scripts/stories.py`:**
- `createNewsletter` - Any logged-in user can create (not admin-only)
- `getNewsletters/<offset>` - Paginated list
- `getNewsletterswSearch/<offset>/<search>` - Search
- `getSpecificNewsletterInfo/<newsletterID>` - Newsletter details
- `getNewsletterStories/<newsletterID>/<offset>` - Stories in newsletter
- `getUserNewsletters/<userID>/<userType>` - User's own newsletters
- `subscribeNewsletter` / `unsubscribeNewsletter` - Subscriptions

**Key differences from Topics:**
- Any logged-in user can create newsletters (not admin-only)
- Only creator can post stories to their newsletter
- Optional `topicID` association
- `newsletterPatrons` table instead of `topicSubscribers`

### Phase 3: Individual Stories
**Files to implement:**
- `/frontend/src/views/Users/UserStories.vue` - Create Story modal, list user's stories
- `/frontend/src/views/SpecificStory.vue` - Full story view with comments

**Backend endpoints to implement:**
- `createStory` - With rich text content, linked drinks, topic/newsletter assignment
- `getStory/<storyID>` - Full story with comments
- `editStory` / `deleteStory` - Author only
- `getUserStories/<userID>/<userType>/<offset>` - User's stories
- `likeStory` / `unlikeStory` - Story likes

### Phase 4: Comments & Engagement
**Backend endpoints to implement:**
- `createStoryComment`
- `getStoryComments/<storyID>`
- `likeStoryComment` / `dislikeStoryComment`
- `deleteStoryComment`

## Tech Stack Reminders:
- **Frontend**: Vue.js 3, vue-router, Bootstrap 5, vue-toastification
- **Backend**: Flask with Blueprints, PostgreSQL, psycopg2 connection pooling
- **Storage**: S3 for images via s3Images module
- **Auth**: localStorage tokens (88B_accID, 88B_accType, 88B_accUsername)

## Files Quick Reference

```
BACKEND:
/backend/scripts/stories.py (PARTIALLY IMPLEMENTED - Topics done)

FRONTEND ROUTER:
/frontend/src/router/modules/story.js
/frontend/src/router/index.js
/frontend/src/router/modules/profile.js

FRONTEND VIEWS - TOPICS (COMPLETE):
/frontend/src/views/BrowseStoryTopics.vue ✅
/frontend/src/views/CreateTopic.vue ✅
/frontend/src/views/SpecificStoryTopic.vue ✅

FRONTEND VIEWS - NEWSLETTERS (TODO):
/frontend/src/views/BrowseStoryNewsletters.vue
/frontend/src/views/CreateNewsletter.vue
/frontend/src/views/SpecificStoryNewsletter.vue

FRONTEND VIEWS - STORIES (TODO):
/frontend/src/views/Users/UserStories.vue
/frontend/src/views/SpecificStory.vue

REFERENCE FILES:
/backend/scripts/assembly.py
/frontend/src/views/BrowseAssemblies.vue
/frontend/src/views/SpecificAssembly.vue
/frontend/src/views/CreateAssembly.vue

DATABASE SCHEMA:
/database/postgresql/final/01-postgresql_data3.sql (lines 2111-2250)
```

## YOUR TASK
Now, your task is to thoroughly study the code (including the BrowseAssembly->SpecificAssembly->Post structrure) so that you can give me the most comprehensive set of clarification questions on my requirements that would enable you to Implement the Newsletters feature (BrowseStoryNewsletters.vue, CreateNewsletter.vue, SpecificStoryNewsletter.vue)



