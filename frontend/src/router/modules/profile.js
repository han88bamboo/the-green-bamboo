
const routes = [
  {
    path: "/profile/user/:userID/:username",
    name: "profileUser",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
    children: [
      {
        path: ":listName?",
        name: "userProfileList",
        component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
      },
      {
        path: "producer_list/:listName",
        name: "userProducerList",
        component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
      },
      {
        path: "venue_list/:listName",
        name: "userVenueList",
        component: () => import(/* webpackChunkName: "profile" */ "@/views/Users/UserProfileRefactor.vue"),
      },
    ]
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
    path: "/profile/venue-refac/:venueID?/:username",
    name: "profileVenueRefac",
    component: () => import(/* webpackChunkName: "profile" */ "@/views/Venues/VenueProfile_refac.vue"),
  }
];

export default routes;
