
const routes = [
  {
    path: '/partner',
    name: 'partnerCenter',
     component: () => import(/* webpackChunkName: "partner" */ '@/views/PartnerCenter.vue')
  },
  {
    path: '/partner/venues',
    name: 'partnerCenterVenues',
     component: () => import(/* webpackChunkName: "partner" */ '@/views/PartnerCenterVenues.vue')
  },
  {
    path: '/partner/brands',
    name: 'partnerCenterBrands',
     component: () => import(/* webpackChunkName: "partner" */ '@/views/PartnerCenterBrands.vue')
  },
  {
    path: '/partner/festivals',
    name: 'partnerCenterFestivals',
     component: () => import(/* webpackChunkName: "partner" */ '@/views/PartnerCenterFestivals.vue')
  },
];

export default routes;
