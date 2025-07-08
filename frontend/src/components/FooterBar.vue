<!--component added by TZH for footer-->

<template>
    
      <footer style="background-color:#ffeccd;" class="row row-cols-1 row-cols-sm-4 py-5  px-5 border-top justify-content-center">
        <div class="col footer-col">
          <!--<a href="/" class="d-flex align-items-center mb-3 link-dark text-decoration-none">
            <svg class="bi me-2" width="40" height="32"><use xlink:href="#bootstrap"></use></svg>
          </a>-->
          <router-link :to="'/'" class=" justify-content-start" style="display: flex !important;">
            <img src="../../Images/Logo/Drink-X Logo.png" style="width: auto; height: 25px;" class="align-self-start mb-3">
          </router-link>
          <ul class="nav justify-content-start list-unstyled ">
            <li class="me-3 mb-3">
              <a class="" href="#">
                <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="black" class="bi bi-facebook" viewBox="0 0 16 16">
                  <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"></path>
                </svg>
              </a>
            </li>
            <li class="me-3 mb-3">
              <a class="" href="#">
                <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="black" class="bi bi-tiktok" viewBox="0 0 16 16">
                  <path d="M9 0h1.98c.144.715.54 1.617 1.235 2.512C12.895 3.389 13.797 4 15 4v2c-1.753 0-3.07-.814-4-1.829V11a5 5 0 1 1-5-5v2a3 3 0 1 0 3 3z"></path>
                </svg>
              </a>
            </li>
            <li class="me-3 mb-3">
              <a class="" href="#">
                <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="black" class="bi bi-facebook" viewBox="0 0 16 16">
                  <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334"></path>
                </svg>
              </a>
            </li>
          </ul>
          <p class="text-black justify-content-start" style="font-weight: bold; display: flex !important;">Drink-X © 2025</p>
        </div>
  
        <div class="col footer-col" >
          <!--<h5>Section</h5>-->
          <ul class="nav flex-column" style="font-weight: bold;">
            
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/help/features" class="nav-link p-0 text-black">Features</a></li>
            <li class="nav-item mb-2 justify-content-start" style="display: flex !important;"><a href="/help/whats-new" class="nav-link p-0 text-black">What's New</a></li>
            <li class="nav-item mb-2 justify-content-start" style="display: flex !important;"><a href="/badges-and-points" class="nav-link p-0 text-black">Badges and Points</a></li>
          </ul>
        </div>
  
        <div class="col footer-col">
          <!--<h5>Section</h5>-->
          <ul class="nav flex-column" style="font-weight: bold; ">
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/partner" class="nav-link p-0 text-black">Partner Center</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/partner/venues" class="nav-link p-0 text-black">Drink-X for Venues</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/partner/brands" class="nav-link p-0 text-black">Drink-X for Brands</a></li>
            
          
          </ul>
        </div>
  
        <div class="col footer-col">
            <!--<h5>Section</h5>-->
          <ul class="nav flex-column" style="font-weight: bold; ">
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/help/about" class="nav-link p-0 text-black">About</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/help/faqs" class="nav-link p-0 text-black">FAQs</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/help/support" class="nav-link p-0 text-black">Support</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/help/terms" class="nav-link p-0 text-black">Terms</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/help/privacy" class="nav-link p-0 text-black">Privacy</a></li>
            <li class="nav-item mb-2  justify-content-start" style="display: flex !important;"><a href="/login" class="nav-link p-0 " style="color:#027562 !important;">Login</a></li>
         
          </ul>
        </div>
      </footer>
    
  </template>
  
  <script>
  export default {
    name: "FooterBar",
  };
  </script>
  
  <style scoped>
  /* Add any custom footer styles here */
  </style>