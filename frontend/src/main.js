// Javascript file that kickstarts application. Imports root component, Bootstrap, and router, and mounts the app to the DOM.

// Import Axios
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { createApp } from 'vue'
import { createHead } from '@unhead/vue/client'
import App from './App.vue'
import router from './router'
import './assets/global.css';
import VueQRCodeComponent from 'vue-qrcode-component'
import VueGoogleMaps from '@fawmi/vue-google-maps'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import 'quill/dist/quill.snow.css';
import { createGtag } from "vue-gtag";

//  Add Google Analytics (GA4)
const gtag = createGtag({
  tagId: "G-FBF3N4940Z",
  router,
})

// Set up Axios as a global property in Vue prototype
const app = createApp(App);
const head = createHead()

// Set up QR code component
app.component('qr-code', VueQRCodeComponent);
app.config.globalProperties.$axios = axios;

// Use plugins
app.use(router);
app.use(gtag); // add Google Analytics
app.use(head); // add SEO for later

console.log("✅ GA plugin initialized");

// Set up Google Maps
app.use(VueGoogleMaps, {
    load: {
        key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
        libraries: 'places', // This is required if you use the Auto complete plug-in
    },
});

// Use Toastification with options
app.use(Toast, {
    transition: "Vue-Toastification__bounce",
    maxToasts: 20,
    newestOnTop: true,
});

// Mount the app to the DOM
app.mount('#app');
