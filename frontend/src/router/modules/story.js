// -----------------------------------------------------------------------------------------
// STORIES FEATURE - Vue Router Module
// -----------------------------------------------------------------------------------------
// Routes for Stories feature (long-form content publishing system)
// 
// Route Structure:
//   /stories/topics                                    → BrowseStoryTopics.vue
//   /stories/topics/create                             → CreateTopic.vue
//   /stories/topics/:topicId/:topicName                → SpecificStoryTopic.vue
//   /stories/newsletters                               → BrowseStoryNewsletters.vue
//   /stories/newsletters/create                        → CreateNewsletter.vue
//   /stories/newsletters/:newsletterId/:newsletterName → SpecificStoryNewsletter.vue
//   /stories/:storyId/:storyTitle                      → SpecificStory.vue
//
// Note: UserStories.vue is registered under profile.js module at:
//   /profile/user/:userID/:username/stories
// -----------------------------------------------------------------------------------------

const routes = [
  // ========================================
  // TOPICS ROUTES
  // ========================================
  {
    path: "/stories/topics",
    name: "browseStoryTopics",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/BrowseStoryTopics.vue"),
    meta: {
      title: "Browse Story Topics"
    }
  },

  {
    path: "/stories/topics/create",
    name: "createTopic",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/CreateTopic.vue"),
    meta: {
      title: "Create Topic",
      requiresAuth: true // TODO: Implement auth check
    }
  },

  {
    path: "/stories/topics/:topicId/:topicName",
    name: "specificStoryTopic",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/SpecificStoryTopic.vue"),
    meta: {
      title: "Topic Stories"
    }
  },

  // ========================================
  // NEWSLETTERS ROUTES
  // ========================================
  {
    path: "/stories/newsletters",
    name: "browseStoryNewsletters",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/BrowseStoryNewsletters.vue"),
    meta: {
      title: "Browse Newsletters"
    }
  },

  {
    path: "/stories/newsletters/create",
    name: "createNewsletter",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/CreateNewsletter.vue"),
    meta: {
      title: "Create Newsletter",
      requiresAuth: true // TODO: Implement auth check
    }
  },

  {
    path: "/stories/newsletters/:newsletterId/:newsletterName",
    name: "specificStoryNewsletter",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/SpecificStoryNewsletter.vue"),
    meta: {
      title: "Newsletter Stories"
    }
  },

  // ========================================
  // INDIVIDUAL STORY ROUTE
  // ========================================
  {
    path: "/stories/:storyId/:storyTitle",
    name: "specificStory",
    component: () => import(/* webpackChunkName: "stories" */ "@/views/SpecificStory.vue"),
    meta: {
      title: "Story"
    }
  },
];

export default routes;
