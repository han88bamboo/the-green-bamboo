// import { mount } from '@vue/test-utils';
// import BottleListings from '../../src/views/Users/BottleListings.vue';

// // COMMAND TO RUN TEST: npm run test:unit

// // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// // -- [TGB-5] VIEW LISTINGS --
// describe('View Listings', () => {

//     // Sample reviews data
//     const all_reviews = [
//         {
//             "_id": {
//                 "$oid": "65b3269dcfdc049a876a7937"
//             },
//             "userID": {
//                 "$oid": "65b327d5687b64f8302d56ef"
//             },
//             "reviewTarget": "Nikka From The Barrel",
//             "date": "1/15/2022",
//             "rating": 2,
//             "reviewDesc": "Not very nice",
//             "taggedUsers": [
//                 "65b327d5687b64f8302d56ee"
//             ],
//             "reviewTitle": "",
//             "reviewType": "",
//             "flavorTag": [],
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b3269dcfdc049a876a7938"
//             },
//             "userID": {
//                 "$oid": "65b327d5687b64f8302d56f0"
//             },
//             "reviewTarget": "Harmony Collection Inspired by Intense Arabica",
//             "date": "1/25/2024",
//             "rating": 5,
//             "reviewDesc": "Best drink ever",
//             "taggedUsers": [
//                 "65b327d5687b64f8302d56ee"
//             ],
//             "reviewTitle": "",
//             "reviewType": "",
//             "flavorTag": [],
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b3269dcfdc049a876a7939"
//             },
//             "userID": {
//                 "$oid": "65b327d5687b64f8302d56ee"
//             },
//             "reviewTarget": "Junglebird",
//             "date": "2/5/2024",
//             "rating": 1,
//             "reviewDesc": "Poor Service",
//             "taggedUsers": [
//                 "65b327d5687b64f8302d56ef"
//             ],
//             "reviewTitle": "",
//             "reviewType": "",
//             "flavorTag": [],
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b3269dcfdc049a876a793a"
//             },
//             "userID": {
//                 "$oid": "65b327d5687b64f8302d56ee"
//             },
//             "reviewTarget": "Malt Grain Cane",
//             "date": "3/4/2024",
//             "rating": 3,
//             "reviewDesc": "Drinks are mediorce",
//             "taggedUsers": [],
//             "reviewTitle": "",
//             "reviewType": "",
//             "flavorTag": [],
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b3269dcfdc049a876a793b"
//             },
//             "userID": {
//                 "$oid": "65b327d5687b64f8302d56ef"
//             },
//             "reviewTarget": "Ube Cream Liqueur",
//             "date": "12/23/2023",
//             "rating": 4,
//             "reviewDesc": "Tasty drink",
//             "taggedUsers": [],
//             "reviewTitle": "",
//             "reviewType": "",
//             "flavorTag": [],
//             "photo": ""
//         }
//     ];

//     // - GET REVIEWS -
//     describe('Get Reviews', () => {

//         // Mock the fetchData method
//         const fetchDataMock = jest.fn(() => Promise.resolve(all_reviews));

//         // Get reviews of listing with reviews
//         it('[Reviews returned] Get reviews of listing with reviews', () => {
//             const wrapper = mount(BottleListings, {
//                 data() {
//                     return {
//                         reviews: all_reviews
//                     };
//                 },
//             });
//             // Mock the listing data
//             const listing = {
//                                 "_id": {
//                                     "$oid": "65b34a06915a4e4e9e08876d"
//                                 },
//                                 "listingName": "Harmony Collection Inspired by Intense Arabica",
//                                 "producerID": {
//                                     "$oid": "65b33f65e8fb649accedb5a9"
//                                 },
//                                 "bottler": "OB",
//                                 "originCountry": "Scotland",
//                                 "drinkType": "Whiskey / Whisky",
//                                 "typeCategory": "Single Malt",
//                                 "age": "NAS",
//                                 "abv": 0.44,
//                                 "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/the-macallan-harmony-collection-inspired-by-intense-arabica-single-malt-44-abv",
//                                 "officialDesc": "The second edition in our limited annual release series, this special single malt exudes flavours of sweet oak, tiramisu and dark chocolate, and provides a delightful whisky and coffee pairing experience.",
//                                 "sourceLink": "",
//                                 "photo": ""
//                             }
//             // Mock the randomReview
//             const randomReview = all_reviews[1];
//             // Call the getReviews method
//             const reviewDesc = wrapper.vm.getReviews(listing);
//             expect(reviewDesc).toBe("Best drink ever");
//         });

//         // Get reviews of listing with no reviews
//         it('[No reviews returned] Get reviews of listing with no reviews', () => {
//             const wrapper = mount(BottleListings, {
//                 data() {
//                     return {
//                         reviews: all_reviews
//                     };
//                 },
//             });
//             // Mock the listing data
//             const listing = {
//                                 "_id": {
//                                     "$oid": "65b34a06915a4e4e9e088787"
//                                 },
//                                 "listingName": "Ardbeg Ardcore",
//                                 "producerID": {
//                                     "$oid": "65b33f65e8fb649accedb5a8"
//                                 },
//                                 "bottler": "OB",
//                                 "originCountry": "Scotland",
//                                 "drinkType": "Whiskey / Whisky",
//                                 "typeCategory": "Single Malt",
//                                 "age": "NAS",
//                                 "abv": 0.46,
//                                 "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/ardbeg-ardcore-46-abv",
//                                 "officialDesc": "From a Distillery with more ups and downs that a pogoing punk comes Ardcore. Created with roasted black malt, roasted to the extreme, this spirit is all about what happens up front & centre stage. The malt is what defines its distinctive profile. Described as tasting like ‘biting on a spiky ball’, Ardcore is a dram that wears its heart on its sleeve… its black heart!",
//                                 "sourceLink": "",
//                                 "photo": ""
//                             }
//             // Mock the randomReview
//             const randomReview = {};
//             // Call the getReviews method
//             const reviewDesc = wrapper.vm.getReviews(listing);
//             expect(reviewDesc).toBe(null);
//         });

//     });

//     // - GET RATINGS -
//     describe('Get Ratings', () => {

//         // Mock the fetchData method
//         const fetchDataMock = jest.fn(() => Promise.resolve(all_reviews));

//         // Get reviews of listing with ratings
//         it('[Ratings returned] Get reviews of listing with ratings', () => {
//             const wrapper = mount(BottleListings, {
//                 data() {
//                     return {
//                         reviews: all_reviews
//                     };
//                 },
//             });
//             // Mock the listing data
//             const listing = {
//                                 "_id": {
//                                     "$oid": "65b34a06915a4e4e9e088785"
//                                 },
//                                 "listingName": "Nikka From The Barrel",
//                                 "producerID": {
//                                     "$oid": "65b33f65e8fb649accedb5a3"
//                                 },
//                                 "bottler": "OB",
//                                 "originCountry": "Japan",
//                                 "drinkType": "Whiskey / Whisky",
//                                 "typeCategory": "Blended",
//                                 "age": "NAS",
//                                 "abv": 0.51,
//                                 "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/nikka-from-the-barrel",
//                                 "officialDesc": "This strong Japanese blend aged in bourbon barrels comes from the blend of two Nikka single malts Miyagikyo and Yoichi and a single grain whisky. Nikka from the Barrel was chosen best Japanese blended whisky under 12 years old at the World Whiskies Awards 2007.",
//                                 "sourceLink": "",
//                                 "photo": ""
//                             }
//             // Mock the ratings data
//             const ratings = {
//                                 "_id": {
//                                     "$oid": "65b3269dcfdc049a876a7937"
//                                 },
//                                 "userID": {
//                                     "$oid": "65b327d5687b64f8302d56ef"
//                                 },
//                                 "reviewTarget": "Nikka From The Barrel",
//                                 "date": "1/15/2022",
//                                 "rating": 2,
//                                 "reviewDesc": "Not very nice",
//                                 "taggedUsers": [
//                                     "65b327d5687b64f8302d56ee"
//                                 ],
//                                 "reviewTitle": "",
//                                 "reviewType": "",
//                                 "flavorTag": [],
//                                 "photo": ""
//                             }
//             // Call the getRatings method
//             const averageRating = wrapper.vm.getRatings(listing);
//             expect(averageRating).toBe(2);
//         });

//         // Get reviews of listing with no ratings
//         it('[No ratings returned] Get reviews of listing with no ratings', () => {
//             const wrapper = mount(BottleListings, {
//                 data() {
//                     return {
//                         reviews: all_reviews
//                     };
//                 },
//             });
//             // Mock the listing data
//             const listing = {
//                                 "_id": {
//                                     "$oid": "65b34a06915a4e4e9e08876f"
//                                 },
//                                 "listingName": "Five Farms Irish Cream Liqueur",
//                                 "producerID": {
//                                     "$oid": "65b33f65e8fb649accedb594"
//                                 },
//                                 "bottler": "OB",
//                                 "originCountry": "Ireland",
//                                 "drinkType": "Liqueur",
//                                 "typeCategory": "Cream",
//                                 "age": "",
//                                 "abv": 0.17,
//                                 "reviewLink": "https://88bamboo.co/blogs/everything-nice/five-farms-irish-cream-liqueur-17",
//                                 "officialDesc": "Exclusively sourced and produced in County Cork, Ireland, Five Farms is the world's first farm-to-table Irish cream liqueur.",
//                                 "sourceLink": "",
//                                 "photo": ""
//                             }
//             // Mock the ratings data
//             const ratings = {}
//             // Call the getRatings method
//             const averageRating = wrapper.vm.getRatings(listing);
//             expect(averageRating).toBe("-");
//         });

//     });

// });

// // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// // --- [TGB-6] SEARCH LISTINGS ---
// describe('Search Listings', () => {
//     // Sample listings data
//     const all_listings = [
//         {
//             "_id": {
//                 "$oid": "65b34a06915a4e4e9e08876d"
//             },
//             "listingName": "Harmony Collection Inspired by Intense Arabica",
//             "producerID": {
//                 "$oid": "65b33f65e8fb649accedb5a9"
//             },
//             "bottler": "OB",
//             "originCountry": "Scotland",
//             "drinkType": "Whiskey / Whisky",
//             "typeCategory": "Single Malt",
//             "age": "NAS",
//             "abv": 0.44,
//             "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/the-macallan-harmony-collection-inspired-by-intense-arabica-single-malt-44-abv",
//             "officialDesc": "The second edition in our limited annual release series, this special single malt exudes flavours of sweet oak, tiramisu and dark chocolate, and provides a delightful whisky and coffee pairing experience.",
//             "sourceLink": "",
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b34a06915a4e4e9e088785"
//             },
//             "listingName": "Nikka From The Barrel",
//             "producerID": {
//                 "$oid": "65b33f65e8fb649accedb5a3"
//             },
//             "bottler": "OB",
//             "originCountry": "Japan",
//             "drinkType": "Whiskey / Whisky",
//             "typeCategory": "Blended",
//             "age": "NAS",
//             "abv": 0.51,
//             "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/nikka-from-the-barrel",
//             "officialDesc": "This strong Japanese blend aged in bourbon barrels comes from the blend of two Nikka single malts Miyagikyo and Yoichi and a single grain whisky. Nikka from the Barrel was chosen best Japanese blended whisky under 12 years old at the World Whiskies Awards 2007.",
//             "sourceLink": "",
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b34a06915a4e4e9e088787"
//             },
//             "listingName": "Ardbeg Ardcore",
//             "producerID": {
//                 "$oid": "65b33f65e8fb649accedb5a8"
//             },
//             "bottler": "OB",
//             "originCountry": "Scotland",
//             "drinkType": "Whiskey / Whisky",
//             "typeCategory": "Single Malt",
//             "age": "NAS",
//             "abv": 0.46,
//             "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/ardbeg-ardcore-46-abv",
//             "officialDesc": "From a Distillery with more ups and downs that a pogoing punk comes Ardcore. Created with roasted black malt, roasted to the extreme, this spirit is all about what happens up front & centre stage. The malt is what defines its distinctive profile. Described as tasting like ‘biting on a spiky ball’, Ardcore is a dram that wears its heart on its sleeve… its black heart!",
//             "sourceLink": "",
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b34a06915a4e4e9e0887bd"
//             },
//             "listingName": "Clase Azul Tequila Reposado",
//             "producerID": {
//                 "$oid": "65b33f65e8fb649accedb5c0"
//             },
//             "bottler": "OB",
//             "originCountry": "Mexico",
//             "drinkType": "Tequila",
//             "typeCategory": "Reposado",
//             "age": "",
//             "abv": 0.4,
//             "reviewLink": "https://88bamboo.co/blogs/tequila-mezcal-reviews/clase-azul-tequila-reposado-40-abv",
//             "officialDesc": "",
//             "sourceLink": "",
//             "photo": ""
//         },
//         {
//             "_id": {
//                 "$oid": "65b34a06915a4e4e9e0887c0"
//             },
//             "listingName": "Tequila Tapatio Excelencia Extra Anejo",
//             "producerID": {
//                 "$oid": "65b33f65e8fb649accedb5b8"
//             },
//             "bottler": "OB",
//             "originCountry": "Mexico",
//             "drinkType": "Tequila",
//             "typeCategory": "Extra Anejo",
//             "age": "",
//             "abv": 0.4,
//             "reviewLink": "https://88bamboo.co/blogs/tequila-mezcal-reviews/tequila-tapatio-excelencia-extra-anejo",
//             "officialDesc": "",
//             "sourceLink": "",
//             "photo": ""
//         },
//         {
//             "_id":{
//                 "$oid": "65b34a06915a4e4e9e088780"
//             },
//             "listingName": "Fords Gin",
//             "producerID": {
//                 "$oid": "65b33f65e8fb649accedb59b"
//             },
//             "bottler": "OB",
//             "originCountry": "United Kingdom",
//             "drinkType": "Gin",
//             "typeCategory": "London Dry / Classic",
//             "age": "",
//             "abv": 0.45,
//             "reviewLink": "",
//             "officialDesc": "Fords Gin is found in the very best gin joints around the world, from iconic hotel bars to frequently visited neighborhood spots. Created with respect to the traditions that have historically defined gin making, this classic London Dry is keen for all your cocktail adventures.",
//             "sourceLink": "",
//             "photo": ""
//         },
//         {   
//             "_id":{
//                 "$oid": "65b34a06915a4e4e9e08877f"
//             },
//             "listingName": "Fords Gin Officers' Reserve",
//             "producerID":{
//                 "$oid": "65b33f65e8fb649accedb59b"
//             },
//             "bottler": "OB",
//             "originCountry": "United Kingdom",
//             "drinkType": "Gin",
//             "typeCategory": "London Dry / Classic",
//             "age": "",
//             "abv": 0.55,
//             "reviewLink": "",
//             "officialDesc": "Over-proof gin was traditionally reserved for officers of the British Royal Navy. Today, it’s for everyone! Fords Gin Officers’ Reserve is rested and aged in Amontillado Sherry casks for three weeks. Characteristics of the barrel’s wood shape the spirit’s flavour. It is then bottled at 54.5 ABV. This limited release is Fords Gin’s first Journey in Gin as a homage to the Navy Strength Gin category.",
//             "sourceLink": "",
//             "photo": ""
//         }
//     ];
//     // Sample producers data
//     const all_producers = [
//         {
//             "_id":{"$oid":"65b33f65e8fb649accedb5a9"},
//             "producerName":"The Macallan Distillery",
//             "producerDesc":"The Macallan distillery is a single malt Scotch whisky distillery in Craigellachie in Moray in the north-east of Scotland. The Macallan Distillers Ltd is a wholly owned subsidiary of Edrington, which purchased the brand from Highland Distillers in 1999.",
//             "originCountry":"Scotland",
//             "statusOB":"",
//             "mainDrinks":"Whisky"
//         },
//         {
//             "_id":{"$oid":"65b33f65e8fb649accedb5a3"},
//             "producerName":"Nikka Whisky",
//             "producerDesc":"",
//             "originCountry":"",
//             "statusOB":"",
//             "mainDrinks":""
//         },
//         {
//             "_id":{"$oid":"65b33f65e8fb649accedb5a8"},
//             "producerName":"Ardbeg Distillery",
//             "producerDesc":"Ardbeg distillery is a Scotch whisky distillery in Ardbeg on the south coast of the isle of Islay, Argyll and Bute, Scotland, in the Inner Hebrides group of islands. The distillery is owned by Louis Vuitton Moët Hennessy, and produces a heavily peated Islay whisky.",
//             "originCountry":"Scotland",
//             "statusOB":"",
//             "mainDrinks":"Whisky"
//         },
//         {
//             "_id":{"$oid":"65b33f65e8fb649accedb5c0"},
//             "producerName":"Clase Azul",
//             "producerDesc":"",
//             "originCountry":"",
//             "statusOB":"",
//             "mainDrinks":""
//         },
//         {
//             "_id":{"$oid":"65b33f65e8fb649accedb5b8"},
//             "producerName":"Tapatio",
//             "producerDesc":"",
//             "originCountry":"",
//             "statusOB":"",
//             "mainDrinks":""
//         },
//         {
//             "_id":{"$oid":"65b33f65e8fb649accedb59b"},
//             "producerName":"Fords Gin",
//             "producerDesc":"",
//             "originCountry":"",
//             "statusOB":"",
//             "mainDrinks":""
//         }
//     ]

//     // Mock the getProducerName(listing) method
//     const getProducerName = jest.fn(listing => {
//         const producerID = listing["producerID"]["$oid"];
//         const producer = all_producers.find(producer => producer["_id"]["$oid"] == producerID);
//         if (producer) {
//             return producer["producerName"];
//         }
//         else {
//             return null;
//         }
//     });

//     // Mock the fetchData method
//     const fetchDataMock = jest.fn(() => Promise.resolve(all_listings));

//     // Search for bottle listing based on Expression Name
//     it('[Listings returned] Search for bottle listing based on Expression Name', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     searchInput: 'Tequila'
//                 };
//             },
//         });
//         // Call the mock getProducerName(listing) method
//         wrapper.vm.getProducerName = getProducerName;
//         // Call the searchListings method
//         wrapper.vm.searchListings();
//         expect(wrapper.vm.filteredListings).toEqual([
//             {
//                 "_id": {
//                     "$oid": "65b34a06915a4e4e9e0887bd"
//                 },
//                 "listingName": "Clase Azul Tequila Reposado",
//                 "producerID": {
//                     "$oid": "65b33f65e8fb649accedb5c0"
//                 },
//                 "bottler": "OB",
//                 "originCountry": "Mexico",
//                 "drinkType": "Tequila",
//                 "typeCategory": "Reposado",
//                 "age": "",
//                 "abv": 0.4,
//                 "reviewLink": "https://88bamboo.co/blogs/tequila-mezcal-reviews/clase-azul-tequila-reposado-40-abv",
//                 "officialDesc": "",
//                 "sourceLink": "",
//                 "photo": ""
//             },
//             {
//                 "_id": {
//                     "$oid": "65b34a06915a4e4e9e0887c0"
//                 },
//                 "listingName": "Tequila Tapatio Excelencia Extra Anejo",
//                 "producerID": {
//                     "$oid": "65b33f65e8fb649accedb5b8"
//                 },
//                 "bottler": "OB",
//                 "originCountry": "Mexico",
//                 "drinkType": "Tequila",
//                 "typeCategory": "Extra Anejo",
//                 "age": "",
//                 "abv": 0.4,
//                 "reviewLink": "https://88bamboo.co/blogs/tequila-mezcal-reviews/tequila-tapatio-excelencia-extra-anejo",
//                 "officialDesc": "",
//                 "sourceLink": "",
//                 "photo": ""
//             }
//         ]);
//     });

//     // Search for bottle listing based on Expression Name, regardless of case
//     it('[Listings returned] Search for bottle listing based on Expression Name, regardless of case', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     searchInput: 'mAcAllan'
//                 };
//             },
//         });
//         // Call the mock getProducerName(listing) method
//         wrapper.vm.getProducerName = getProducerName;
//         // Call the searchListings method
//         wrapper.vm.searchListings();
//         expect(wrapper.vm.filteredListings).toEqual([
//             {
//                 "_id": {
//                     "$oid": "65b34a06915a4e4e9e08876d"
//                 },
//                 "listingName": "Harmony Collection Inspired by Intense Arabica",
//                 "producerID": {
//                     "$oid": "65b33f65e8fb649accedb5a9"
//                 },
//                 "bottler": "OB",
//                 "originCountry": "Scotland",
//                 "drinkType": "Whiskey / Whisky",
//                 "typeCategory": "Single Malt",
//                 "age": "NAS",
//                 "abv": 0.44,
//                 "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/the-macallan-harmony-collection-inspired-by-intense-arabica-single-malt-44-abv",
//                 "officialDesc": "The second edition in our limited annual release series, this special single malt exudes flavours of sweet oak, tiramisu and dark chocolate, and provides a delightful whisky and coffee pairing experience.",
//                 "sourceLink": "",
//                 "photo": ""
//             }
//         ]);
//     });

//     // Search for bottle listing based on Producer
//     it('[Listings returned] Search for bottle listing based on Producer', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     searchInput: 'Fords Gin'
//                 };
//             },
//         });
//         // Call the mock getProducerName(listing) method
//         wrapper.vm.getProducerName = getProducerName;
//         // Call the searchListings method
//         wrapper.vm.searchListings();
//         expect(wrapper.vm.filteredListings).toEqual([
//             {
//                 "_id":{
//                     "$oid": "65b34a06915a4e4e9e088780"
//                 },
//                 "listingName": "Fords Gin",
//                 "producerID": {
//                     "$oid": "65b33f65e8fb649accedb59b"
//                 },
//                 "bottler": "OB",
//                 "originCountry": "United Kingdom",
//                 "drinkType": "Gin",
//                 "typeCategory": "London Dry / Classic",
//                 "age": "",
//                 "abv": 0.45,
//                 "reviewLink": "",
//                 "officialDesc": "Fords Gin is found in the very best gin joints around the world, from iconic hotel bars to frequently visited neighborhood spots. Created with respect to the traditions that have historically defined gin making, this classic London Dry is keen for all your cocktail adventures.",
//                 "sourceLink": "",
//                 "photo": ""
//             },
//             {   
//                 "_id":{
//                     "$oid": "65b34a06915a4e4e9e08877f"
//                 },
//                 "listingName": "Fords Gin Officers' Reserve",
//                 "producerID":{
//                     "$oid": "65b33f65e8fb649accedb59b"
//                 },
//                 "bottler": "OB",
//                 "originCountry": "United Kingdom",
//                 "drinkType": "Gin",
//                 "typeCategory": "London Dry / Classic",
//                 "age": "",
//                 "abv": 0.55,
//                 "reviewLink": "",
//                 "officialDesc": "Over-proof gin was traditionally reserved for officers of the British Royal Navy. Today, it’s for everyone! Fords Gin Officers’ Reserve is rested and aged in Amontillado Sherry casks for three weeks. Characteristics of the barrel’s wood shape the spirit’s flavour. It is then bottled at 54.5 ABV. This limited release is Fords Gin’s first Journey in Gin as a homage to the Navy Strength Gin category.",
//                 "sourceLink": "",
//                 "photo": ""
//             }
//         ]);
//     });

//     // Search for bottle listing based on Producer, regardless of case
//     it('[Listings returned] Search for bottle listing based on Producer, regardless of case', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     searchInput: 'niKKA fROM the BARrel'
//                 };
//             },
//         });
//         // Call the mock getProducerName(listing) method
//         wrapper.vm.getProducerName = getProducerName;
//         // Call the searchListings method
//         wrapper.vm.searchListings();
//         expect(wrapper.vm.filteredListings).toEqual([
//             {
//                 "_id": {
//                     "$oid": "65b34a06915a4e4e9e088785"
//                 },
//                 "listingName": "Nikka From The Barrel",
//                 "producerID": {
//                     "$oid": "65b33f65e8fb649accedb5a3"
//                 },
//                 "bottler": "OB",
//                 "originCountry": "Japan",
//                 "drinkType": "Whiskey / Whisky",
//                 "typeCategory": "Blended",
//                 "age": "NAS",
//                 "abv": 0.51,
//                 "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/nikka-from-the-barrel",
//                 "officialDesc": "This strong Japanese blend aged in bourbon barrels comes from the blend of two Nikka single malts Miyagikyo and Yoichi and a single grain whisky. Nikka from the Barrel was chosen best Japanese blended whisky under 12 years old at the World Whiskies Awards 2007.",
//                 "sourceLink": "",
//                 "photo": ""
//             }
//         ]);
//     });

//     // Search for specific bottle listings that do not exist
//     it('[No listings returned] Search for specific bottle listings that do not exist', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     searchInput: 'nothing'
//                 };
//             },
//         });
//         // Call the mock getProducerName(listing) method
//         wrapper.vm.getProducerName = getProducerName;
//         // Call the searchListings method
//         wrapper.vm.searchListings();
//         expect(wrapper.vm.searchResults).toStrictEqual([]);
//     });

//     // Search for nothing (blank input)
//     it('[No listings returned] Search for nothing (blank input)', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     searchInput: ''
//                 };
//             },
//         });
//         // Call the mock getProducerName(listing) method
//         wrapper.vm.getProducerName = getProducerName;
//         // Call the searchListings method
//         wrapper.vm.searchListings();
//         expect(wrapper.vm.searchResults).toStrictEqual([]);
//     });
// });

// // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------