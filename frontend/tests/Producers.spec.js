// import { mount } from '@vue/test-utils';
// import BottleListings from '../../src/views/Producers/BottleListings.vue';


// // COMMAND TO RUN TEST: npm run test:unit

// // -------------------------------------------------------------------------------------------------------------------------------------------------

// // -- [TGB-7] WHERE TO BUY --
// describe('Where To Buy', () => {
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
//             "_id": {
//                 "$oid": "65b33f65e8fb649accedb5a9"
//             },
//             "producerName": "The Macallan Distillery",
//             "producerDesc": "The Macallan distillery is a single malt Scotch whisky distillery in Craigellachie in Moray in the north-east of Scotland. The Macallan Distillers Ltd is a wholly owned subsidiary of Edrington, which purchased the brand from Highland Distillers in 1999.",
//             "originCountry": "Scotland",
//             "statusOB": "",
//             "mainDrinks":"Whisky"
//         },
//         {
//             "_id": {
//                 "$oid":"65b33f65e8fb649accedb5a3"
//             },
//             "producerName": "Nikka Whisky",
//             "producerDesc": "",
//             "originCountry": "",
//             "statusOB": "",
//             "mainDrinks": ""
//         },
//         {
//             "_id": {
//                 "$oid":"65b33f65e8fb649accedb5a8"
//             },
//             "producerName": "Ardbeg Distillery",
//             "producerDesc": "Ardbeg distillery is a Scotch whisky distillery in Ardbeg on the south coast of the isle of Islay, Argyll and Bute, Scotland, in the Inner Hebrides group of islands. The distillery is owned by Louis Vuitton Moët Hennessy, and produces a heavily peated Islay whisky.",
//             "originCountry": "Scotland",
//             "statusOB": "",
//             "mainDrinks": "Whisky"
//         },
//         {
//             "_id": {
//                 "$oid":"65b33f65e8fb649accedb5c0"
//             },
//             "producerName": "Clase Azul",
//             "producerDesc": "",
//             "originCountry": "",
//             "statusOB": "",
//             "mainDrinks": ""
//         },
//         {
//             "_id": {
//                 "$oid":"65b33f65e8fb649accedb5b8"
//             },
//             "producerName": "Tapatio",
//             "producerDesc": "",
//             "originCountry": "",
//             "statusOB": "",
//             "mainDrinks": ""
//         },
//         {
//             "_id": {
//                 "$oid":"65b33f65e8fb649accedb59b"
//             },
//             "producerName": "Fords Gin",
//             "producerDesc": "",
//             "originCountry": "",
//             "statusOB": "",
//             "mainDrinks": ""
//         }
//     ]

//     // Mock the fetchData method
//     const fetchDataMock = jest.fn(() => Promise.resolve(all_listings));

//     // Search for Producers based on specified listing
//     it('[Listings returned] Search for Producers based on specified listing', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     specified_listing:  {
//                                             "_id": {
//                                                 "$oid": "65b34a06915a4e4e9e088787"
//                                             },
//                                             "listingName": "Ardbeg Ardcore",
//                                             "producerID": {
//                                                 "$oid": "65b33f65e8fb649accedb5a8"
//                                             },
//                                             "bottler": "OB",
//                                             "originCountry": "Scotland",
//                                             "drinkType": "Whiskey / Whisky",
//                                             "typeCategory": "Single Malt",
//                                             "age": "NAS",
//                                             "abv": 0.46,
//                                             "reviewLink": "https://88bamboo.co/blogs/whisky-reviews/ardbeg-ardcore-46-abv",
//                                             "officialDesc": "From a Distillery with more ups and downs that a pogoing punk comes Ardcore. Created with roasted black malt, roasted to the extreme, this spirit is all about what happens up front & centre stage. The malt is what defines its distinctive profile. Described as tasting like ‘biting on a spiky ball’, Ardcore is a dram that wears its heart on its sleeve… its black heart!",
//                                             "sourceLink": "",
//                                             "photo": ""
//                                         }
//                 };
//             },
//         });
//         // Call the whereToBuy method
//         wrapper.vm.whereToBuy();
//         expect(wrapper.vm.producerListings).toEqual([{"$oid":"65b33f65e8fb649accedb5a8"}]);
//     });

//     // Search for Producers that do not exist based on specified listing
//     it('[No listings returned] Search for Producers that do not exist based on specified listing', () => {
//         const wrapper = mount(BottleListings, {
//             data() {
//                 return {
//                     listings: all_listings,
//                     specified_listing:  {
//                                             "_id": {
//                                                 "$oid": "65b34a06915a4e4e9e08877c"
//                                             },
//                                             "listingName": "KI NO BI Kyoto Dry Gin",
//                                             "producerID": {
//                                                 "$oid":"65b33f65e8fb649accedb599"
//                                             },
//                                             "bottler": "OB",
//                                             "originCountry": "Japan",
//                                             "drinkType": "Gin",
//                                             "typeCategory": "Contemporary",
//                                             "age": "","abv": 0.46,
//                                             "reviewLink": "",
//                                             "officialDesc": "KI NO BI (“The Beauty of the Seasons”) is inspired by tradition and is distilled, blended and bottled in Kyoto. Our gin is made in a recognisably dry style, but with a distinct Japanese accent. KI NO BI Kyoto Dry Gin is created with Japanese botanicals such as yellow yuzu from the north of Kyoto Prefecture, akamatsu wood chips (Japanese red pine), bamboo, gyokuro tea from the Uji region and green sanshō (Japanese peppercorn) berries.",
//                                             "sourceLink": "",
//                                             "photo": ""
//                                         }
//                 };
//             },
//         });
//         // Call the whereToBuy method
//         wrapper.vm.whereToBuy();
//         expect(wrapper.vm.producerListings).toEqual([]);
//     });

// });

// // -------------------------------------------------------------------------------------------------------------------------------------------------
