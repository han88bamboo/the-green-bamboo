
const routes = [
  {
    path: "/profile/user/:userID/:username",
    name: "profileUser",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
  },
  {
    path: "/profile/user/:userID/:username/allreviews",
    name: "allReviews",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/AllReviews.vue"),
  },
  {
    path: "/profile/user/:userID/:username/allfollowingfollowers",
    name: "allFollowingFollowers",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/AllFollowingFollowers.vue"),
  },
  {
    path: "/profile/user/:userID/:username/producer_list/:listName",
    name: "userProducerList",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
  },
  {
    path: "/profile/user/:userID/:username/venue_list/:listName",
    name: "userVenueList",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
  },
  {
    path: "/profile/user/:userID/:username/:listName?",
    name: "userProfileList",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
  },
  {
    path: "/profile/producer/:producerID/:username",
    name: "profileProducer",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Producers/ProducerProfile.vue"),
  },
  {
    path: "/profile/venue/:venueID?/:username",
    name: "profileVenue",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Venues/VenueProfile.vue"),
  },
  {
    path: "/venue/:venueID/event-report",
    name: "eventReport",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Venues/EventReport.vue"),
  },
  // { - refactored venue profile commented out for now 
  //   path: "/profile/venue-refac/:venueID?/:username",
  //   name: "profileVenueRefac",
  //   component: () => import(/* webpackChunkName: "profile" */ "@/views/Venues/VenueProfile_refac.vue"),
  // },
  {
    path: "/home/profile",
    name: "homeProfile",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/HomeProfile.vue"),
  }
];

export default routes;
