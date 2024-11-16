-- Insert color values into the "colours" table
INSERT INTO "colours" ("hexcode") VALUES
('#FFFFFF'),
('#FEED97'),
('#FBE166'),
('#FAD74A'),
('#F5C84B'),
('#F8C139'),
('#E79E12'),
('#E07D1F'),
('#D55530'),
('#B63426'),
('#AA1F22'),
('#702C1C'),
('#4A1C0C'),
('#000000');

-- Insert country values into the "countries" table
INSERT INTO "countries" ("originCountry", "legalAge") VALUES
('Albania', 18),
('Algeria', 18),
('Andorra', 18),
('Angola', 18),
('Antigua and Barbuda', 16),
('Argentina', 18),
('Armenia', 18),
('Australia', 18),
('Austria', 16),
('Azerbaijan', 18),
('Bahrain', 21),
('Bangladesh', 18),
('Barbados', 16),
('Belarus', 18),
('Belgium', 16),
('Belize', 18),
('Benin', 20),
('Bhutan', 18),
('Bolivia', 18),
('Bosnia and Herzegovina', 18),
('Botswana', 18),
('Brazil', 18),
('Brunei', 18),
('Bulgaria', 18),
('Burkina Faso', 18),
('Burundi', 16),
('Cabo Verde', 18),
('Cambodia', 21),
('Cameroon', 21),
('Canada', 19),
('Central African Republic', 16),
('Chad', 16),
('Channel Islands', 18),
('Chile', 18),
('China', 18),
('Colombia', 18),
('Comoros', 18),
('Costa Rica', 18),
('Côte d''Ivoire', 18),
('Croatia', 18),
('Cuba', 16),
('Cyprus', 18),
('Czech Republic', 18),
('Democratic Republic of the Congo', 18),
('Denmark', 16),
('Dominica', 16),
('Dominican Republic', 18),
('Ecuador', 18),
('Egypt', 21),
('El Salvador', 18),
('Equatorial Guinea', 18),
('Eritrea', 25),
('Estonia', 18),
('Eswatini', 18),
('Ethiopia', 18),
('Faeroe Islands', 18),
('Fiji', 18),
('Finland', 18),
('France', 18),
('Gabon', 18),
('Gambia', 18),
('Georgia', 16),
('Germany', 16),
('Ghana', 18),
('Gibraltar', 18),
('Greece', 18),
('Grenada', 18),
('Guadeloupe', 18),
('Guatemala', 18),
('Guinea', 18),
('Guyana', 18),
('Haiti', 16),
('Honduras', 18),
('Hong Kong', 18),
('Hungary', 18),
('Iceland', 20),
('India', 21),
('Indonesia', 21),
('Iraq', 21),
('Ireland', 18),
('Isle of Man', 18),
('Israel', 18),
('Italy', 18),
('Ivory Coast', 18),
('Jamaica', 18),
('Japan', 20),
('Jordan', 18),
('Kazakhstan', 21),
('Kenya', 18),
('Kuwait', 21),
('Kyrgyzstan', 18),
('Laos', 18),
('Latvia', 18),
('Lebanon', 18),
('Lesotho', 21),
('Liberia', 18),
('Liechtenstein', 18),
('Lithuania', 18),
('Luxembourg', 16),
('Macao', 18),
('Madagascar', 18),
('Malawi', 18),
('Malaysia', 18),
('Maldives', 18),
('Mali', 16),
('Malta', 17),
('Marshall Islands', 21),
('Mauritania', 21),
('Mauritius', 18),
('Mexico', 18),
('Moldova', 18),
('Monaco', 18),
('Mongolia', 18),
('Montenegro', 18),
('Morocco', 18),
('Mozambique', 18),
('Myanmar', 18),
('Namibia', 18),
('Nauru', 21),
('Nepal', 18),
('Netherlands', 18),
('New Zealand', 18),
('Nicaragua', 18),
('Niger', 18),
('Nigeria', 18),
('North Korea', 18),
('Norway', 18),
('Oman', 21),
('Pakistan', 18),
('Palau', 21),
('Palestine', 16),
('Panama', 18),
('Papua New Guinea', 18),
('Paraguay', 20),
('Peru', 18),
('Philippines', 18),
('Poland', 18),
('Portugal', 18),
('Puerto Rico', 18),
('Qatar', 19),
('Republic of Macedonia', 18),
('Republic of the Congo', 18),
('Romania', 18),
('Russia', 18),
('Rwanda', 18),
('Saint Kitts and Nevis', 18),
('Saint Lucia', 16),
('Saint Vincent and the Grenadines', 18),
('San Marino', 16),
('São Tomé and Príncipe', 18),
('Senegal', 18),
('Serbia', 18),
('Seychelles', 18),
('Sierra Leone', 18),
('Singapore', 18),
('Slovakia', 18),
('Slovenia', 18),
('Solomon Islands', 21),
('South Africa', 18),
('South Korea', 19),
('South Sudan', 18),
('Spain', 18),
('Sri Lanka', 21),
('Suriname', 16),
('Sweden', 18),
('Switzerland', 16),
('Syria', 18),
('Taiwan', 18),
('Tajikistan', 18),
('Tanzania', 18),
('Thailand', 20),
('The Bahamas', 18),
('Timor-Leste', 18),
('Togo', 18),
('Trinidad and Tobago', 18),
('Tunisia', 18),
('Turkey', 18),
('Turkmenistan', 18),
('Uganda', 18),
('Ukraine', 18),
('United Arab Emirates', 21),
('United Kingdom', 18),
('United States of America', 21),
('Uruguay', 18),
('Uzbekistan', 20),
('Venezuela', 18),
('Vietnam', 18),
('Zambia', 18),
('Zimbabwe', 18);

-- Insert serving type values into the "servingTypes" table
INSERT INTO "servingTypes" ("servingType") VALUES
('Glass'),
('Bottle'),
('Can'),
('Dram'),
('Pint'),
('Shot'),
('In A Cocktail'),
('Serving');

-- Insert special color values into the "specialColours" table
INSERT INTO "specialColours" ("hexList", "colour") VALUES
(ARRAY['#24FF00', '#074202'], 'green'),
(ARRAY['#FF0F0F', '#69140F'], 'red'),
(ARRAY['#8F8DF3', '#051B6B'], 'darkblue'),
(ARRAY['#82E3E9', '#0A7E97'], 'lightblue'),
(ARRAY['#FDC1FE', '#AD1181'], 'pink'),
(ARRAY['#CBA4E3', '#5B0E8A'], 'purple');

-- Insert flavor tag values into the "flavourTags" table
INSERT INTO "flavourTags" ("hexcode", "familyTag") VALUES
('#CE5858', 'Common'),
('#A6C4D5', 'Floral'),
('#E78181', 'Fruits'),
('#71966B', 'Green'),
('#C97ECB', 'Confectionary'),
('#DD9E54', 'Cereal'), 
('#774326', 'Earthy'),
('#9C7A52', 'Spices'),
('#6B9691', 'Mineral'),
('#CEC69F', 'Lactic'),
('#326A55', 'Umami'),
('#80839E', 'Smoky'),
('#BCAF35', 'Others');

-- Insert tags into the subTags table with familyTagId 1
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(1, 'Sweet'),
(1, 'Sour'),
(1, 'Salty'),
(1, 'Umami'),
(1, 'Bitter'),
(1, 'Rich'),
(1, 'Thin'),
(1, 'Light'),
(1, 'Thick'),
(1, 'Mellow'),
(1, 'Hot'),
(1, 'Juicy'),
(1, 'Candied'),
(1, 'Rounded'),
(1, 'Full-Bodied');

-- Insert tags into the subTags table with familyTagId 2
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(2, 'White Flowers'),
(2, 'Yellow Flowers'),
(2, 'Red Flowers'),
(2, 'Purple Flowers'),
(2, 'Field Flowers'),
(2, 'Dried Flowers'),
(2, 'Exotic Flowers'),
(2, 'Oriental Flowers'),
(2, 'Pine Forest'),
(2, 'Rainforest'),
(2, 'Potpourri'),
(2, 'Bouquet'),
(2, 'Beeswax'),
(2, 'Fruit Flowers'),
(2, 'Perfume');

-- Insert tags into the subTags table with familyTagId 3
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(3, 'Sweet Berries'),
(3, 'Tinned Fruit'),
(3, 'Orchard Fruits'),
(3, 'Stone Fruits'),
(3, 'Tropical Fruits'),
(3, 'Green Fruits'),
(3, 'Citrus'),
(3, 'Yellow Fruits'),
(3, 'Unripe Fruits'),
(3, 'Dried Fruits'),
(3, 'Stewed Fruits'),
(3, 'Melons'),
(3, 'Coconut'),
(3, 'Tart Fruits'),
(3, 'Sweet Wine');

-- Insert tags into the subTags table with familyTagId 4
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(4, 'Fresh Herbs'),
(4, 'Dried Herbs'),
(4, 'Vegetables'),
(4, 'Leafy'),
(4, 'Hay'),
(4, 'Meadow'),
(4, 'Grassy'),
(4, 'Minty'),
(4, 'Hops'),
(4, 'Succulent'),
(4, 'Olive'),
(4, 'Green Tea'),
(4, 'Pith'),
(4, 'Sugarcane'),
(4, 'Juniper');

-- Insert tags into the subTags table with familyTagId 5
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(5, 'Caramel'),
(5, 'Toffee'),
(5, 'Candy'),
(5, 'Syrup'),
(5, 'Treacle'),
(5, 'Brown Sugar'),
(5, 'Nougat'),
(5, 'Baked Goods'),
(5, 'Custard'),
(5, 'Milk Chocolate'),
(5, 'Fruit Cake'),
(5, 'Vanilla Cream'),
(5, 'Maple Syrup'),
(5, 'Honey'),
(5, 'Cola Syrup');

-- Insert tags into the subTags table with familyTagId 6
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(6, 'Sweet Grain'),
(6, 'Spicy Grain'),
(6, 'Husk'),
(6, 'Nutty'),
(6, 'Fresh Bread'),
(6, 'Burnt Toast'),
(6, 'Biscuits'),
(6, 'Rice'),
(6, 'Cooked Mash'),
(6, 'Steamed Rice'),
(6, 'Sweet Corn'),
(6, 'Cooked Barley'),
(6, 'Rustic'),
(6, 'Butter Cookies'),
(6, 'Porridge');

-- Insert tags into the subTags table with familyTagId 7
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(7, 'Old Wood'),
(7, 'Damp Wood'),
(7, 'Charred Wood'),
(7, 'Coffee'),
(7, 'Lacquer'),
(7, 'Musty'),
(7, 'Wood Shaving'),
(7, 'Soil'),
(7, 'Incense'),
(7, 'Tobacco'),
(7, 'Cacao'),
(7, 'Oaky'),
(7, 'Leather'),
(7, 'Vines'),
(7, 'Resinous');

-- Insert tags into the subTags table with familyTagId 8
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(8, 'Sweet Herbal'),
(8, 'Bitter Herbal'),
(8, 'Roots'),
(8, 'Pepper'),
(8, 'Baking Spices'),
(8, 'Cinnamon'),
(8, 'Black Tea'),
(8, 'Clove'),
(8, 'Anise'),
(8, 'Ginger'),
(8, 'Liquorice'),
(8, 'Nutmeg'),
(8, 'Chilli'),
(8, 'Oriental Spice'),
(8, 'Mediterranean Spice');

-- Insert tags into the subTags table with familyTagId 9
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(9, 'Antiseptic'),
(9, 'Wet Stone'),
(9, 'Chalk'),
(9, 'Concrete'),
(9, 'Briney'),
(9, 'Oysters'),
(9, 'Coastal'),
(9, 'Rainwater'),
(9, 'Mineral Water'),
(9, 'Clay'),
(9, 'Wax'),
(9, 'Asphalt'),
(9, 'Isotonic'),
(9, 'Gravel'),
(9, 'Crisp Water');

-- Insert tags into the subTags table with familyTagId 10
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(10, 'Farmhouse'),
(10, 'Sweat'),
(10, 'Yeasty'),
(10, 'Soft Cheese'),
(10, 'Yogurt'),
(10, 'Dough'),
(10, 'Koji'),
(10, 'Balsamic'),
(10, 'Fermented'),
(10, 'Butter'),
(10, 'Milky'),
(10, 'Sour Cream'),
(10, 'Sauerkraut'),
(10, 'Lees'),
(10, 'Pickled');

-- Insert tags into the subTags table with familyTagId 11
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(11, 'Hard Cheese'),
(11, 'Miso'),
(11, 'Mushroom'),
(11, 'Soy Sauce'),
(11, 'Seaweed'),
(11, 'Boiled Egg'),
(11, 'Bean Paste'),
(11, 'Charcuterie Meat'),
(11, 'Bonito Flakes'),
(11, 'Broth'),
(11, 'Black Olives'),
(11, 'Anchovy'),
(11, 'Oyster Sauce'),
(11, 'Marmite'),
(11, 'Sundried Tomatoes');

-- Insert tags into the subTags table with familyTagId 12
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(12, 'Industrial'),
(12, 'Barbecue'),
(12, 'Sweet Smoke'),
(12, 'Cold Ash'),
(12, 'Smoked Fish'),
(12, 'Bitter Ash'),
(12, 'Roasted Chestnuts'),
(12, 'Heavy Roast Coffee'),
(12, 'Burnt Vegetal'),
(12, 'Burnt Sugar'),
(12, 'Cigar'),
(12, 'Toasted Nuts'),
(12, 'Smoke'),
(12, 'Savoury'),
(12, 'Scented Candles');

-- Insert tags into the subTags table with familyTagId 13
INSERT INTO "subTags" ("familyTagId", "subTag") VALUES
(13, 'Tannic'),
(13, 'Solvent'),
(13, 'Plastic'),
(13, 'Coal Gas'),
(13, 'Shoe Polish'),
(13, 'Rubber'),
(13, 'Tar'),
(13, 'Skunky'),
(13, 'Metallic'),
(13, 'Glue'),
(13, 'Varnish'),
(13, 'Soap'),
(13, 'Sulphur'),
(13, 'Oxidized'),
(13, 'Cardboard');


-- Insert all language values into the "languages" table
INSERT INTO "languages" ("language") VALUES
('Corsican'),
('Aymara'),
('Croatian'),
('Czech'),
('Georgian'),
('Igbo'),
('Samoan'),
('Shona'),
('Western Frisian'),
('Estonian'),
('Romanian'),
('Sinhala'),
('Amharic'),
('Bhojpuri'),
('Catalan'),
('Filipino'),
('Hebrew'),
('Malayalam'),
('Hindi'),
('Irish'),
('Krio'),
('Malay'),
('Portuguese'),
('Tsonga'),
('Ukrainian'),
('Uyghur'),
('Xhosa'),
('Cebuano'),
('Divehi'),
('Guarani'),
('Khmer'),
('Kyrgyz'),
('Maithili'),
('Tigrinya'),
('Urdu'),
('Zulu'),
('Kazakh'),
('Korean'),
('Marathi'),
('Norwegian'),
('Southern Sotho'),
('Swahili'),
('Turkish'),
('Albanian'),
('Arabic'),
('Azerbaijani'),
('Bangla'),
('Bulgarian'),
('Greek'),
('Lao'),
('Somali'),
('Assamese'),
('Danish'),
('English'),
('Finnish'),
('Hawaiian'),
('Hungarian'),
('Icelandic'),
('Italian'),
('Japanese'),
('Kannada'),
('Kurdish'),
('Northern Sotho'),
('Nyanja'),
('Haitian Creole'),
('Latvian'),
('Scottish Gaelic'),
('Slovenian'),
('Uzbek'),
('Yoruba'),
('Basque'),
('Esperanto'),
('Gujarati'),
('Javanese'),
('Maltese'),
('Serbian'),
('Tajik'),
('Tamil'),
('Hausa'),
('Iloko'),
('Kinyarwanda'),
('Mongolian'),
('Russian'),
('Bambara'),
('Central Kurdish'),
('Chinese (Traditional)'),
('Ewe'),
('French'),
('Indonesian'),
('Luxembourgish'),
('Nepali'),
('Punjabi'),
('Sindhi'),
('Telugu'),
('Welsh'),
('Akan'),
('Bosnian'),
('Dogri'),
('Galician'),
('Ganda'),
('German'),
('Macedonian'),
('Māori'),
('Mizo'),
('Pashto'),
('Thai'),
('Turkmen'),
('Vietnamese'),
('Burmese'),
('Hmong'),
('Malagasy'),
('Odia'),
('Polish'),
('Sundanese'),
('Swedish'),
('Afrikaans'),
('Belarusian'),
('Chinese (Simplified)'),
('Dutch'),
('Goan Konkani'),
('Lingala'),
('Manipuri (Meitei Mayek)'),
('Spanish'),
('Tatar'),
('Armenian'),
('Latin'),
('Lithuanian'),
('Oromo'),
('Persian'),
('Quechua'),
('Sanskrit'),
('Slovak'),
('Yiddish');

-- Insert observation tags into the observationTags table
INSERT INTO "observationTags" ("observationTag") VALUES
('Beginner Friendly'),
('Recommended for Enthusiasts'),
('Good for Gifts 🎁'),
('Cool Packaging'),
('Acquired Taste 🤭'),
('Easy to Drink 😋'),
('Good for Cocktails 🍸'),
('Good for Sipping 🥃'),
('Good for Highballs 🍹'),
('More Complex Than Inception'),
('Sharp Like a Toothpick'),
('Hot Like Hell 🔥'),
('Ticket to Funkytown 🎟️'),
('Food Pairing Friendly 🥩'),
('Broke the Bank 💰'),
('Smooth Criminal 🕺🏻'),
('Grail 😇'),
('Unique Expression ⭐'),
('What Just Hit Me'),
('For My Worst Enemy 😡'),
('Overhyped! 🥸'),
('Try Once'),
('Is This Water?🚰'),
('Daily Drinker'),
('Netflix & Chill 🍆'),
('Healthy');

INSERT INTO "users" ("username","displayName","choiceDrinks","modType","photo","hashedPassword","joinDate","firstName","lastName","email","isAdmin","birthday","pin") VALUES
	 ('admin','admin','{}','{}','','-1522920846','2024-10-28 18:45:31.403','admin','admin','admin@drink-x.com',false,'2000-01-01 00:00:00','175029,2024-10-28 18:46:29'),
	 ('Lotusroot518','Lotusroot518','{}','{}','','-289780632','2024-10-29 01:31:56.379','Lotusroot518','Lotusroot518','Kailinchoo@gmail.com',true,'1995-08-11 00:00:00',NULL),
	 ('charsiucharlie','charsiucharlie','{}','{}','','-65180891','2024-10-30 13:48:46.277','charsiucharlie','charsiucharlie','tzhehan@gmail.com',true,'1993-06-29 00:00:00',NULL),
	 ('DumplingBoy','DumplingBoy','{}','{}','','2108394495','2024-11-03 09:49:51.179','DumplingBoy','DumplingBoy','jwleong.199@gmail.com',false,'1999-10-21 00:00:00',NULL);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Whiskey / Whisky',                           -- drinkType
    NULL,                                         -- badgePhoto (set a URL if available)
    ARRAY[
        'Single Malt',
        'Single Grain',
        'Blended Malt',
        'Blended Grain',
        'Blended Malt & Grain',
        'Single Blended (Malt & Grain from the Same Distillery)',
        'Irish Pot Still Whisk(e)y',
        'Irish Blended Whisk(e)y',
        'Bourbon Whisk(e)y',
        'Tennessee Whisk(e)y',
        'Rye Whisk(e)y',
        'Rye Malt Whisk(e)y',
        'Malt Whisk(e)y',
        'Corn Whisk(e)y',
        'Wheat Whisk(e)y',
        'American Whisk(e)y (Others)',
        'Rice Whisk(e)y',
        'Flavoured',
        'New Make / Moonshine / White Dog',
        'Others'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Whiskey / Whisky',                           -- drinkType
    NULL,                                         -- badgePhoto (set a URL if available)
    ARRAY[
        'Single Malt',
        'Single Grain',
        'Blended Malt',
        'Blended Grain',
        'Blended Malt & Grain',
        'Single Blended (Malt & Grain from the Same Distillery)',
        'Irish Pot Still Whisk(e)y',
        'Irish Blended Whisk(e)y',
        'Bourbon Whisk(e)y',
        'Tennessee Whisk(e)y',
        'Rye Whisk(e)y',
        'Rye Malt Whisk(e)y',
        'Malt Whisk(e)y',
        'Corn Whisk(e)y',
        'Wheat Whisk(e)y',
        'American Whisk(e)y (Others)',
        'Rice Whisk(e)y',
        'Flavoured',
        'New Make / Moonshine / White Dog',
        'Others'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Cocktails',                                 -- drinkType
    NULL,                                        -- badgePhoto (set a URL if available)
    ARRAY[
        'Classics',
        'Punch',
        'Milk Punch',
        'Sling',
        'Sour',
        'Cobbler',
        'Highball',
        'Highball - Canned'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Tequila',                                   -- drinkType
    NULL,                                        -- badgePhoto (set a URL if available)
    ARRAY[
        'Blanco (Unaged / White)',
        'Joven / Oro (Young / Gold)',
        'Reposado (Aged)',
        'Añejo (Extra Aged)',
        'Extra Añejo (Ultra Aged)',
        'Cristalino',
        'Curado (Flavoured)',
        'Others'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Rum / Rhum',                                -- drinkType
    NULL,                                        -- badgePhoto (set a URL if available)
    ARRAY[
        'Juice - Rhum Agricole (Column Still)',
        'Juice - Pure Single Rum (Pot Still)',
        'Juice - Single Blended Rum (Pot & Column Still)',
        'Juice - All Others (Excluding White Unaged and Including Multi-Distillery Blend, Excluding Clairin / Cachaca / Aguardiente)',
        'Juice - White Unaged',
        'Syrup - Traditional Rum (Column Still)',
        'Syrup - Pure Single Rum (Pot Still)',
        'Syrup - Single Blended Rum (Pot & Column Still)',
        'Syrup - All Others (Excluding White Unaged and Including Multi-Distillery Blend, Excluding Clairin / Cachaca / Aguardiente)',
        'Syrup - White / Unaged',
        'Syrup / Juice - Clairin / Cachaca / Aguardiente',
        'Molasses - Traditional Rum (Column Still)',
        'Molasses - Pure Single Rum (Pot Still)',
        'Molasses - Single Blended Rum (Pot & Column Still)',
        'Molasses - All Others (Excluding White Unaged and Including Multi-Distillery Blend)',
        'Molasses - White Unaged',
        'Others - Excluding 100% Juice / 100% Syrup / 100% Molasses',
        'Flavoured / Spiced',
        'White Unaged Blend of Molasses, Juice, and/or Syrup'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Beer', -- drinkType
    NULL, -- badgePhoto (replace with a URL if applicable)
    ARRAY[
        'Aged Beer',
        'Ale - All Styles',
        'Altbier - All Styles',
        'Barleywine - All Styles',
        'Barrel Aged Beer',
        'Belgian Style - Blonde / Brown / Dark Ale',
        'Belgian Style - Contemporary Spontaneous Fermented',
        'Belgian Style - Dubbel',
        'Belgian Style - Golden Ale',
        'Belgian Style - Quadrupel',
        'Belgian Style - Saison',
        'Belgian Style - Tripel',
        'Belgian Style - All Others',
        'Bitter Ale - All Styles',
        'Blonde Ale',
        'Brett Beer',
        'Brown Ale - All Styles',
        'California Common / Steam Beer',
        'Cider - Aged / Barrel Aged',
        'Cider - Apfelwein / German Style',
        'Cider - Cidre / French Style',
        'Cider - Dry',
        'Cider - Fruited / Flavoured',
        'Cider - Graff',
        'Cider - Herbed / Spiced',
        'Cider - Hopped',
        'Cider - Ice',
        'Cider - Mulled',
        'Cider - Perry',
        'Cider - Poiré',
        'Cider - Pommeau',
        'Cider - Rosé',
        'Cider - Sitra / Spanish Style',
        'Cider - Sour',
        'Cider - Sweet',
        'Cider - Traditional',
        'Cider - All Others',
        'Cider - Other Fruit',
        'Corn Beer / Chicha de Jora',
        'Cream Ale',
        'Dark Ale',
        'Farmhouse Ale - Bière de Coupage',
        'Farmhouse Ale - Bière de Garde',
        'Farmhouse Ale - Bière de Mars',
        'Farmhouse Ale - Classic French & Belgian Style',
        'Farmhouse Ale - Finnish Style Sahti',
        'Farmhouse Ale - Grisette',
        'Farmhouse Ale - Saison',
        'Farmhouse Ale - All Others',
        'Field Beer',
        'Flavored Malt Beverage',
        'Freeze-Distilled Beer',
        'Fruit Beer',
        'German Style - Bock',
        'German Style - Doppelbock',
        'German Style - Eisbock',
        'German Style - Festbier',
        'German Style - Helles Bock / Maibock',
        'German Style - Historical',
        'German Style - Kellerbier / Zwickelbier',
        'German Style - Kölsch / Koelsch',
        'German Style - Märzen',
        'German Style - Oktoberfestbier/Wiesn',
        'German Style - Rauchbier',
        'German Style - Roggenbier',
        'German Style - Rotbier',
        'German Style - Schwarzbier',
        'German Style - All Others',
        'Ginger Beer / Hard Ginger Beer',
        'Golden Ale - All Styles',
        'Grape Ale - All Styles',
        'Grodziskie / Grätzer',
        'Happoshu',
        'Hard Kombucha',
        'Hard Seltzer',
        'Historical Beer - All Others',
        'Honey Beer',
        'Hybrid Beer / Hybrid Style Beer / Hybrid Lager / Hybrid Ale',
        'IPA (India Pale Ale)',
        'IPA - American Style (All)',
        'IPA - Barrel Aged',
        'IPA - Belgian Style',
        'IPA - Black / Cascadian Dark Ale',
        'IPA - Brett',
        'IPA - Brown',
        'IPA - Brut',
        'IPA - Cold',
        'IPA - Double (DIPA) / Imperial',
        'IPA - Double Dry Hopped (DDH)',
        'IPA - Dry Hopped',
        'IPA - Fruited',
        'IPA - New England / Hazy / Juicy',
        'IPA - Hazy Double (DIPA)',
        'IPA - Hazy Triple (TIPA)',
        'IPA - Milkshake / Double Milkshake / Imperial',
        'IPA - Quadruple',
        'IPA - Red',
        'IPA - Rye',
        'IPA - Session',
        'IPA - Single Hop',
        'IPA - Sour',
        'IPA - Triple (TIPA)',
        'IPA - Triple Dry Hopped (TDH)',
        'IPA - West Coast',
        'IPA - White / Wheat',
        'IPA - All Others',
        'Koji Beer / Ginjo Beer / Sake Yeast Beer',
        'Kvass',
        'Lager - Amber / Red',
        'Lager - American Style (All Styles)',
        'Lager - Dark',
        'Lager - Dortmunder / Export',
        'Lager - Dunkel',
        'Lager - European Style',
        'Lager - Helles',
        'Lager - IPL (India Pale Lager)',
        'Lager - Japanese Rice / All Rice',
        'Lager - Leichtbier',
        'Lager - Mexican',
        'Lager - Pale',
        'Lager - Strong',
        'Lager - Vienna Style',
        'Lager - Winter',
        'Lager - All Others',
        'Lambic - Framboise',
        'Lambic - Other Fruit',
        'Lambic - Gueuze',
        'Lambic - Kriek',
        'Lambic - All Others',
        'Malt Beverage - All Styles',
        'Mead - Traditional / Sack / Great / Imperial / Session',
        'Mead - Fruited',
        'Mead - Herbed & Spiced',
        'Mild Ale - All Styles',
        'Non Alcohlic - Lager',
        'Non Alcoholic - Beer',
        'Non Alcoholic - Cider',
        'Non Alcoholic - IPA',
        'Non Alcoholic - Malt Beverage',
        'Non Alcoholic - Mead',
        'Non Alcoholic - Pale Ale',
        'Non Alcoholic - Porter',
        'Non Alcoholic - Sour',
        'Non Alcoholic - Stout',
        'Non Alcoholic - Wheat Beer',
        'Non Alcoholic - All Others',
        'Old Ale',
        'Pale Ale - All American Styles',
        'Pale Ale - All Australian Style',
        'Pale Ale - Barrel Aged',
        'Pale Ale - All Belgian Styles',
        'Pale Ale - English Style',
        'Pale Ale - Hazy / Juicy',
        'Pale Ale - Milkshake',
        'Pale Ale - All Others',
        'Pilsner - All Styles',
        'Porter - All Styles',
        'Stout',
        'Stout - Barrel Aged',
        'Stout - Foreign / Export',
        'Stout - Imperial / Double',
        'Stout - Imperial / Pastry',
        'Stout - Oyster',
        'Stout - Pastry',
        'Pumpkin Beer',
        'Red Ale - American Style / American Amber',
        'Red Ale - Imperial / Double',
        'Red Ale - All Others',
        'Root Beer',
        'Rye Beer',
        'Scotch Ale - Export',
        'Scotch Ale - Heavy / Wee Heavy',
        'Scotch Ale - Light',
        'Shandy / Radler',
        'Smoke Beer / Smoked Beer',
        'Sorghum / Millet Beer',
        'Sour - American Style (All)',
        'Sour - Barrel Aged',
        'Sour - Berliner Weisse / Fruited',
        'Sour - Flanders Oud Bruin / Oud Red Ale',
        'Sour - Fruited',
        'Sour - Gose (All)',
        'Sour - Smoothie / Pastry',
        'Sour - All Others',
        'Specialty Beer - All Styles',
        'Specialty Grain',
        'Squash Beer',
        'Strong Ale - All Others',
        'Summer Ale - All Styles',
        'Table Beer / Small Beer',
        'Wheat Beer - American Style',
        'Wheat Beer - German / Bavarian Style',
        'Wheat Beer - All Others',
        'Wild Beer / Wild Ale - All Styles',
        'Yam Beer'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Shochu', -- drinkType
    NULL, -- badgePhoto (replace with a URL if applicable)
    ARRAY[
        'Mugi (Barley)',
        'Imo (Sweet Potato)',
        'Kome (Rice)',
        'Soba (Buckwheat)',
        'Kokuto (Brown Sugar)',
        'Kuri (Chestnut)',
        'Awamori (Jasmine Rice Okinawan Shochu)',
        'Kasutori (Sake lees)',
        'Flavoured',
        'Kusu (Aged Awamori)',
        'Shisho (Perilla)',
        'All Others (Undisclosed ingredients Incl. milk, perilla, sesame, corn, sugarcane etc)',
        'Kasu (Sake Lees)'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Sake', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Futsushu (Table sakes) & All Others – NOT including Flavoured',
        'Honjozo (Alcohol added)',
        'Junmai',
        'Ginjo (Alcohol added)',
        'Junmai Ginjo',
        'Daiginjo (Alcohol added)',
        'Junmai Daiginjo',
        'Only Nigori (Cloudy) – all grades, NOT including Sparkling-Nigori, NOT including Kijoshu-Nigori',
        'Only Sparkling – all grades, NOT including Sparkling-Nigori, NOT including Kijoshu-Sparkling',
        'Only Sparkling-Nigoris – all grades',
        'Only Kijoshu (Concentrated) – all grades, including Kijoshu-Nigori or Kijoshu-Sparkling sakes',
        'Amazake',
        'Doburoku',
        'Flavoured (Umeshu sakes, fruit-flavoured sakes, flavoured nigoris, others)',
        'Uncategorised',
        'Komodaru (Traditional Barrel Aged)'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Soju', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Modern (Grocery store soju, usually in green glass bottles)',
        'Craft (Small batch distilled, not matured)',
        'Flavoured',
        'Traditional (Onggi Matured)',
        'Barrel Aged'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Makgeolli & Korean Rice Wines', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Modern Makgeolli/Takju (Grocery store makgeolli) - Unflavoured',
        'Artisanal Makgeolli/Takju (Craft, Traditional)',
        'Cheongju / Yakju (Clarified Makgeolli)',
        'Flavoured Makgeolli - All types'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Wine (Grape wine)', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Red Wine - Single Varietal',
        'Red Wine - Blend of Varietals',
        'White Wine - Single Varietal',
        'White Wine - Blend of Varietals',
        'Orange Wine - Single Varietal',
        'Orange Wine - Blend of Varietals',
        'Rosé - Single Varietal',
        'Rosé - Blend of Varietals',
        'Sparkling White (Incl Champagne) - Single Varietal, NOT natural wine',
        'Sparkling White (Incl Champagne) - Blend of Varietals, NOT natural wine',
        'Sparkling Rosé - Single Varietal, NOT natural wine',
        'Sparkling Rosé - Blend of Varietals, NOT natural wine',
        'Sparkling Red - Single Varietal, NOT natural wine',
        'Sparkling Red - Blend of Varietals, NOT natural wine',
        'Fortified Wine (Incl. Port, Sherry, Apera) - Single Varietal',
        'Fortified Wine (Incl. Port, Sherry, Apera) - Blend of Varietals',
        'Only Natural Wine (Incl. Pét Nat, Organic, Biodynamic) – All grades, all colours, including sparkling',
        'All Others'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Brandy', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Armagnac - Bas-Armagnac',
        'Armagnac - Haut-Armagnac',
        'Armagnac - Ténarèze',
        'Armagnac - Blend',
        'Armagnac - All Others / Undisclosed Region',
        'Cognac - Single Estate',
        'Cognac - Blend',
        'Cognac - All Others / Undisclosed Region',
        'Grappa / Pomace / Marc Brandy - Mono-Varietal',
        'Grappa / Pomace / Marc Brandy - Poli-Varietal',
        'Grappa / Pomace / Marc Brandy - All Others / Undisclosed Varietal',
        'Pisco - Puro',
        'Pisco - Acholado',
        'Pisco - Mosto Verde',
        'Pisco - All Others / Undisclosed Varietal',
        'Calvados - Pays d''Auge',
        'Calvados - Domfrontais',
        'Calvados - Blend',
        'Calvados - All Others / Undisclosed Region',
        'All Others - Aged',
        'All Others - Unaged',
        'All Others - Flavoured'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Baijiu', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Strong Aroma (Nong Xiang)',
        'Light Aroma (Qing Xiang)',
        'Sauce Aroma (Jiang Xiang)',
        'Rice Aroma (Mi Xiang)',
        'Sesame Aroma (Zhima Xiang)',
        'Phoenix Aroma (Feng Xiang)',
        'Fat Aroma (Zhi Xiang)',
        'Medicinal Aroma (Yao Xiang)',
        'Mixed Aroma (Jian Xiang)',
        'All Others (Including Baijiu Liqueur)'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Vodka', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Classic',
        'Infused',
        'Flavoured',
        'Barrel Aged'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'Liqueur', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Cream',
        'Coffee',
        'Chocolate',
        'Fruit',
        'Herbs & Spices',
        'Floral',
        'Nuts',
        'Others'
    ]
);

INSERT INTO "drinkTypes" ("drinkType", "badgePhoto", "typeCategory")
VALUES (
    'All Other Drinks', -- drinkType
    NULL, -- badgePhoto (replace with a URL if needed)
    ARRAY[
        'Absinthe',
        'Arrack',
        'Ready-To-Drink Cocktails (Canned Chuhai, Canned Negroni, etc)',
        'Other Spirits (Feni, Huangjiu etc)',
        'Other Fermented Drinks (Palm Wine, Pulque, etc)',
        'Destilado de Agave (unregistered ''mezcals'')',
        'Sotol'
    ]
);

INSERT INTO "producers" (
    "id", 
    "producerName", 
    "producerDesc", 
    "originCountry", 
    "mainDrinks", 
    "photo", 
    "hashedPassword", 
    "claimStatus", 
    "claimStatusCheckDate", 
    "statusOB", 
    "username", 
    "producerLink", 
    "stripeCustomerId"
) VALUES (
    1, 
    'Hennessy', 
    'This is Hennessy', 
    'France', 
    '{}', 
    NULL, 
    '-6552510', 
    true, 
    NULL, 
    NULL, 
    'Hennessy', 
    '', 
    NULL
);

INSERT INTO "venues" (
    "id", 
    "venueName", 
    "address", 
    "venueType", 
    "originLocation", 
    "venueDesc", 
    "hashedPassword", 
    "photo", 
    "claimStatus", 
    "claimStatusCheckDate", 
    "reservationDetails", 
    "username", 
    "publicHolidays", 
    "stripeCustomerId", 
    "pin"
) VALUES (
    1, 
    'Orh Gao Taproom', 
    'Singapore', 
    'Bar', 
    'Singapore', 
    'Best venue for drinks', 
    '-1918297408', 
    NULL, 
    true, 
    NULL, 
    'Cannot reserve anything', 
    'orhgaotaproom', 
    'Not open on Christmas', 
    NULL, 
    NULL
);

INSERT INTO "producersQuestionAnswers" (
	"id", "question", "answer", "date", "userId", "producerId")
    VALUES (1, 'When are you going to release the next promotion?', 'SOON! CHECK FOR UPDATES!', '2024-10-04 16:08:59.899', 1, 1);

INSERT INTO "listings" (
	"id", "listingName", "producerID", "bottler", "originCountry", "drinkType", "abv", "officialDesc", "allowMod", "addedDate", "typeCategory", "age", "reviewLink", "sourceLink", "photo")
	VALUES (1, 'Hennessy VS', 1, 'OB', 'Japan', 'Whiskey', 12, 'BEST EVEERRRR', true, '2024-10-05 00:14:37.661786', 'Spirit', 12, '', '', '');

INSERT INTO "usersFollowLists" (
    "id", "userId", "users", "producers", "venues")
    VALUES (1, 1, '{}', '{}', '{}'), (2, 2, '{}', '{}', '{}'), (3, 3, '{}', '{}', '{}'), (4, 4, '{}', '{}', '{}');

INSERT INTO "usersDrinkLists" (
    "id", "userId", "listName", "drinks")
    VALUES 
    (1, 1, 'Drinks I Have Tried', '{}'), 
    (2, 1, 'Drinks I Want To Try', '{}'), 
    (3, 2, 'Drinks I Have Tried', '{}'), 
    (4, 2, 'Drinks I Want To Try', '{}'), 
    (5, 3, 'Drinks I Have Tried', '{}'), 
    (6, 3, 'Drinks I Want To Try', '{}'), 
    (7, 4, 'Drinks I Have Tried', '{}'), 
    (8, 4, 'Drinks I Want To Try', '{}');

INSERT INTO "venuesMenu" (
    "id","sectionName", "sectionOrder","venueId")
    VALUES(1, 'Created1', '0', 1);
    
INSERT INTO "menuItems"(
    "id", "itemOrder", "itemPrice", "itemAvailability", "itemID", "itemServingType", "sectionId")
VALUES(1, 0, 12.00, true, 1, 1, 1)