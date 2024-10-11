// import { mount } from '@vue/test-utils';
// import LoginPage from '../../src/views/LoginPage.vue';

// // Mock window.location.href
// delete window.location;
// window.location = { href: '' };

// // COMMAND TO RUN TEST: npm run test:unit

// // -------------------------------------------------------------------------------------------------------------------------------------------------

// // -- [TGB-35] VIEW LOGIN PAGE --

// describe('View Login Page', () => {
//     // Mock data
//     // User
//     const user_data = [
//         {   "_id": {"$oid": "65b327d5687b64f8302d56ee"},
//             username: "111hotpot", 
//             hashedPassword: "-1531949234", 
//         },
//     ];
//     // Producer
//     const producer_data = [
//         {   "_id": {"$oid": "65b33f65e8fb649accedb5a9"},
//             producerName: "The Macallan Distillery", 
//             hashedPassword: "629677616", 
//         },
//     ]
//     // Venue
//     const venue_data = [
//         { 
//             "_id": {"$oid": "65b3333752012c9f2c3d2eb1"},
//             venueName: "GudSht", 
//             hashedPassword: "1457245014", 
//         },
//     ]

//     // Mock objects
//     const user = { ID: "111hotpot", password: "westlife123", role: "user" }
//     const producer = { ID: "The Macallan Distillery", password: "macallan!d1st1llery",  role: "producer" }
//     const venue = { ID: "GudSht", password: "datssomegdshit",  role: "venue" }

//     // - NO ROLE SELECTED -
//     // No role selected for user
//     it('[User] No role selected', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: "", // --> [ERR!] No role selected
//                     ID: user.ID,
//                     password: user.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Role is selected
//         expect(wrapper.vm.errors).toContain("No role selected");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // No role selected for producer
//     it('[Producer] No role selected', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: "", // --> [ERR!] No role selected
//                     ID: producer.ID,
//                     password: producer.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Role is selected
//         expect(wrapper.vm.errors).toContain("No role selected");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // No role selected for venue
//     it('[Venue] No role selected', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: "", // --> [ERR!] No role selected
//                     ID: venue.ID,
//                     password: venue.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Role is selected
//         expect(wrapper.vm.errors).toContain("No role selected");
//         // Clear localStorage
//         localStorage.clear();
//     });


//     // - NO USERNAME ENTERED -
//     // No username entered for user
//     it('[User] No username entered', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: user.role,
//                     ID: "", // --> [ERR!] No Username entered
//                     password: user.password,
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Trigger the hashPassword method

//         // Expect an error message indicating that no Username is entered
//         expect(wrapper.vm.errors).toContain("No username entered");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // No username entered for producer
//     it('[Producer] No username entered', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: producer.role,
//                     ID: "", // --> [ERR!] No Username entered
//                     password: producer.password,
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Username is entered
//         expect(wrapper.vm.errors).toContain("No username entered");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // No username entered for venue
//     it('[Venue] No username entered', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: venue.role,
//                     ID: "", // --> [ERR!] No Username entered
//                     password: venue.password,
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Username is entered
//         expect(wrapper.vm.errors).toContain("No username entered");
//         // Clear localStorage
//         localStorage.clear();
//     });

//     // - NO PASSWORD ENTERED -
//     // No password entered for user
//     it('[User] No password entered', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: user.role,
//                     ID: user.ID,
//                     password: "", // --> [ERR!] No password entered
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Password is entered
//         expect(wrapper.vm.errors).toContain("No password entered");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // No password entered for producer
//     it('[Producer] No password entered', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: producer.role,
//                     ID: producer.ID,
//                     password: "", // --> [ERR!] No password entered
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Password is entered
//         expect(wrapper.vm.errors).toContain("No password entered");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // No password entered for venue
//     it('[Venue] No password entered', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: venue.role,
//                     ID: venue.ID,
//                     Password: "", // --> [ERR!] No password entered
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that no Password is entered
//         expect(wrapper.vm.errors).toContain("No password entered");
//         // Clear localStorage
//         localStorage.clear();
//     });

//     // - INVALID USERNAME -
//     // Invalid username for user
//     it('[User] Invalid username', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: user.role,
//                     ID: "loltesting", // --> [ERR!] Invalid username
//                     password: user.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that username is invalid
//         expect(wrapper.vm.errors).toContain("Invalid username or password");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // Invalid username for producer
//     it('[Producer] Invalid username', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: producer.role,
//                     ID: "loltesting", // --> [ERR!] Invalid username
//                     password: producer.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that username is invalid
//         expect(wrapper.vm.errors).toContain("Invalid username or password");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // Invalid username for venue
//     it('[Venue] Invalid username', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: venue.role,
//                     ID: "loltesting", // --> [ERR!] Invalid username
//                     password: venue.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that username is invalid
//         expect(wrapper.vm.errors).toContain("Invalid username or password");
//         // Clear localStorage
//         localStorage.clear();
//     });

//     // - INVALID PASSWORD -
//     // Invalid password for user
//     it('[User] Invalid password', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: user.role,
//                     ID: user.ID,
//                     password: "loltesting",  // --> [ERR!] Invalid password
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that username is invalid
//         expect(wrapper.vm.errors).toContain("Invalid username or password");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // Invalid password for producer
//     it('[Producer] Invalid password', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: producer.role,
//                     ID: producer.ID,
//                     password: "loltesting",  // --> [ERR!] Invalid password
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that username is invalid
//         expect(wrapper.vm.errors).toContain("Invalid username or password");
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // Invalid password for venue
//     it('[Venue] Invalid password', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: venue.role,
//                     ID: venue.ID,
//                     password: "loltesting",  // --> [ERR!] Invalid password
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect an error message indicating that username is invalid
//         expect(wrapper.vm.errors).toContain("Invalid username or password");
//         // Clear localStorage
//         localStorage.clear();
//     });

//     // - NO ERRORS -
//     // Valid login for user
//     it('[User] Valid login', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: user.role,
//                     ID: user.ID,
//                     password: user.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect no error messages
//         expect(wrapper.vm.errors).toEqual([]);
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // Valid login for producer
//     it('[Producer] Valid login', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: producer.role,
//                     ID: producer.ID,
//                     password: producer.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect no error messages
//         expect(wrapper.vm.errors).toEqual([]);
//         // Clear localStorage
//         localStorage.clear();
//     });
//     // Valid login for venue
//     it('[Venue] Valid login', () => {
//         const wrapper = mount(LoginPage, {
//             data() {
//                 return {
//                     // Data from mock database
//                     users: user_data,
//                     producers: producer_data,
//                     venues: venue_data,
//                     // Test case data
//                     role: venue.role,
//                     ID: venue.ID,
//                     password: venue.password, 
//                     // Error handling
//                     errors: [],
//                 };
//             },
//         });
//         // Trigger the checkRole method
//         wrapper.vm.checkLogin();
//         // Expect no error messages
//         expect(wrapper.vm.errors).toEqual([]);
//         // Clear localStorage
//         localStorage.clear();
//     });

// });