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
    "question", "answer", "date", "userId", "producerId")
    VALUES ('When are you going to release the next promotion?', 'SOON! CHECK FOR UPDATES!', '2024-10-04 16:08:59.899', 1, 1);

INSERT INTO "listings" (
    "listingName", "producerID", "bottler", "originCountry", "drinkType", "abv", "officialDesc", "allowMod", "addedDate", "typeCategory", "age", "reviewLink", "sourceLink", "photo")
	VALUES ('Hennessy VS', 1, 'OB', 'Japan', 'Whiskey', 12, 'BEST EVEERRRR', true, '2024-10-05 00:14:37.661786', 'Spirit', 12, '', '', '');

insert into "reviews" (
"id", "userID", "reviewTarget", "rating", "reviewDesc", "reviewType", "createdDate", "language", "finish", "willRecommend", "wouldBuyAgain", "taggedUsers", "flavourTag", "photo", "colour", "aroma", "location", "taste", "observationTag", "address")
values (21, 1, 1, 5, 'This was absolutely fantastic!', 'Listing', '2025-01-13 18:27:38.498', 'English', 'Long, alittle more oaky now', true, false, '{}', '{}', '', '', '', null, '', '{Beginner Friendly}', '');

INSERT INTO "usersFollowLists" (
    "userId", "users", "producers", "venues")
    VALUES (1, '{}', '{}', '{}'), (2, '{}', '{}', '{}'), (3, '{}', '{}', '{}'), (4, '{}', '{}', '{}');

INSERT INTO "usersDrinkLists" (
    "userId", "listName", "drinks")
    VALUES 
    (1, 'Drinks I Have Tried', '{}'), 
    (1, 'Drinks I Want To Try', '{}'), 
    (2, 'Drinks I Have Tried', '{}'), 
    (2, 'Drinks I Want To Try', '{}'), 
    (3, 'Drinks I Have Tried', '{}'), 
    (3, 'Drinks I Want To Try', '{}'), 
    (4, 'Drinks I Have Tried', '{}'), 
    (4, 'Drinks I Want To Try', '{}');

INSERT INTO "venuesMenu" (
    "sectionName", "sectionOrder","venueId")
    VALUES('Created1', '0', 1);
    
INSERT INTO "menuItems"(
    "itemOrder", "itemPrice", "itemAvailability", "itemID", "itemServingType", "sectionId")
VALUES(0, 12.00, true, 1, 1, 1);

INSERT INTO "clubs"(
    "clubName", "clubDesc", "isInviteOnly", "clubLink", "clubBanner", "dateCreated")
VALUES
    ('Beer Enthusiasts', 'A club for fans of craft beers and brewing techniques', false, 'www.beerclub.com', '', '2024-10-29 19:00:31.403'),
    ('Wine Connoisseurs', 'Explore the world of fine wines, tastings, and pairings', true, 'www.wineclub.com', '', '2024-10-30 20:10:31.403'),
    ('Scotch Aficionados', 'Scotch lovers unite! Share and learn about premium scotches', false, 'www.scotchclub.com', '', '2024-11-01 15:25:31.403'),
    ('Rum Admirers', 'A community for those who enjoy classic and modern rums', false, 'www.rumclub.com', '', '2024-11-03 17:35:31.403'),
    ('Whisky Women', 'Empowering women to explore and enjoy whisky', true, 'www.whiskywomen.com', '', '2024-11-05 14:40:31.403'),
    ('Tequila Tribe', 'Dive into the rich flavors and traditions of tequila', false, 'www.tequilatribe.com', '', '2024-11-07 16:20:31.403'),
    ('Cocktail Creators', 'For mixologists and cocktail enthusiasts of all levels', true, 'www.cocktailclub.com', '', '2024-11-10 13:15:31.403'),
    ('Brandy Lovers', 'Discover and celebrate the elegance of brandy', false, 'www.brandyclub.com', '', '2024-11-12 12:30:31.403'),
    ('Gin Explorers', 'A group for gin enthusiasts and curious tasters', false, 'www.ginclub.com', '', '2024-11-15 14:50:31.403'),
    ('Bourbon Fans', 'Bourbon lovers, join us for tastings and discussions', false, 'www.bourbonclub.com', '', '2024-11-17 18:45:31.403'),
    ('Cognac Circle', 'Share your passion for cognac with fellow enthusiasts', true, 'www.cognacclub.com', '', '2024-11-20 19:30:31.403'),
    ('Whisky Journeys', 'Explore whiskies from around the world', false, 'www.whiskyjourneys.com', '', '2024-11-23 20:00:31.403'),
    ('Sake Society', 'Dive into the art and tradition of sake', false, 'www.sakesociety.com', '', '2024-11-25 11:20:31.403'),
    ('Craft Beer Co-op', 'Discover unique craft beers from local brewers', true, 'www.craftbeercoop.com', '', '2024-11-28 16:30:31.403'),
    ('Homebrewers Hub', 'A space for homebrewers to exchange tips and ideas', false, 'www.homebrewclub.com', '', '2024-12-01 18:25:31.403'),
    ('Liquor Legends', 'Discuss and appreciate rare and legendary liquors', false, 'www.liquorlegends.com', '', '2024-12-03 14:50:31.403'),
    ('Distillery Discoverers', 'For those who love touring distilleries and tasting', true, 'www.distilleryclub.com', '', '2024-12-05 15:30:31.403'),
    ('Vintage Spirits', 'A club dedicated to collecting and tasting vintage spirits', true, 'www.vintagespiritsclub.com', '', '2024-12-07 17:45:31.403'),
    ('Amaro Aficionados', 'For fans of bitters, aperitifs, and amaro culture', false, 'www.amaroaficionados.com', '', '2024-12-10 19:15:31.403'),
    ('Spirit Collectors', 'A community for collectors of unique and rare spirits', true, 'www.spiritcollectors.com', '', '2024-12-13 18:10:31.403'),
    ('Highball Society', 'The perfect club for highball cocktail lovers', false, 'www.highballsociety.com', '', '2024-12-15 15:25:31.403'),
    ('Port & Sherry Lovers', 'Explore the depths of port and sherry flavors', true, 'www.portsherryclub.com', '', '2024-12-17 12:35:31.403'),
    ('Absinthe Advocates', 'A mysterious journey into absinthe culture and history', false, 'www.absintheclub.com', '', '2024-12-20 11:45:31.403'),
    ('Malt Masters', 'Dive deep into the intricacies of malt beverages', false, 'www.maltmasters.com', '', '2024-12-22 10:20:31.403'),
    ('Mocktail Makers', 'For those who enjoy crafting and drinking mocktails', false, 'www.mocktailclub.com', '', '2024-12-23 16:50:31.403'),
    ('Prosecco Pals', 'A bubbly club for prosecco lovers', false, 'www.proseccopals.com', '', '2024-12-24 15:15:31.403'),
    ('Sparkling Spirits', 'A vibrant community for lovers of sparkling beverages', true, 'www.sparklingspirits.com', '', '2024-12-25 14:10:31.403'),
    ('Whisky 101', 'Begin your whisky journey with us!', false, 'www.whisky101club.com', '', '2024-12-26 14:30:31.403'),
    ('Rum Rebels', 'Discover the rebellious side of rum culture', false, 'www.rumrebels.com', '', '2024-12-27 18:45:31.403'),
    ('Barrel Aged Fans', 'Uncover the flavors of barrel-aged drinks', true, 'www.barrelagedfans.com', '', '2024-12-28 19:20:31.403');


INSERT INTO "clubMembers"(
    "clubID", "userID", "userType", "joinDate", "isAdmin", "joinStatus")
VALUES
    (1, 1, 'user', '2024-10-28 18:47:31.403', true, true),
    (1, 2, 'user', '2024-10-30 18:45:31.403', false, true),
    (1, 3, 'user', '2024-10-30 18:45:31.403', false, false),
    (1, 1, 'venue', '2024-10-30 18:53:31.403', false, false),
    (1, 1, 'producer', '2024-10-30 18:53:31.403', false, false),
    (2, 1, 'producer', '2024-10-28 18:55:31.403', true, true);

INSERT INTO "clubPosts"(
    "clubID", "postDate", "postContent", "postPhotos", "posterID")
VALUES 
    (1, '2024-10-31 18:45:31.403', 'First taste of Yamazaki 12-Year\n\nSmooth with notes of honesy, dried fruits, vanilla, and a touch of spice. Enjoyed it neat - how do you prefer yours?\n\nAny recommendations for what I should try next?', '{}', 1),
    (1, '2024-10-31 19:00:31.403', 'Tried Glenfiddich 15-Year tonight. The sherry cask influence is incredible! Any other whiskies with a strong sherry profile I should try?', '{}', 2),
    (1, '2024-11-01 20:15:31.403', 'Enjoyed a dram of Ardbeg 10-Year. That smoky, peaty kick is unreal! Who else loves Islay whiskies?', '{}', 3),
    (1, '2024-11-02 18:30:31.403', 'Finally tried Maker’s Mark. Sweet, easy to drink, but I’m curious—how does it compare to Buffalo Trace?', '{}', 4),
    (1, '2024-11-03 19:45:31.403', 'Visited a local distillery today and tried their new single malt. A bit young but promising. Anyone else into independent distilleries?', '{}', 1),
    (1, '2024-11-04 21:00:31.403', 'Thinking of hosting a whisky tasting night. What’s the best way to organize the tasting order?', '{}', 2),
    (1, '2024-11-05 17:20:31.403', 'Macallan Double Cask 12-Year was on my list today. Smooth, sweet, and a perfect after-dinner drink. What’s your go-to dessert whisky?', '{}', 3),
    (1, '2024-11-06 19:10:31.403', 'Tried Laphroaig Quarter Cask. It’s bold, smoky, and unforgettable. What’s the best food pairing for such a peaty whisky?', '{}', 4),
    (1, '2024-11-07 20:50:31.403', 'Experimented with a whisky sour using Woodford Reserve. Turned out great! Do you prefer your whisky straight or in cocktails?', '{}', 1),
    (1, '2024-11-08 18:25:31.403', 'Had my first taste of Highland Park 18-Year. Truly balanced with honey, peat, and spice. Is the 21-Year worth the splurge?', '{}', 2),
    (1, '2024-11-09 19:30:31.403', 'For beginners: Glenlivet 12-Year is a great start. What would you recommend as a next step up?', '{}', 3),
    (1, '2024-11-10 20:45:31.403', 'Attended a whisky festival today! Tried so many new brands. Who else loves whisky events?', '{}', 4),
    (1, '2024-11-11 18:15:31.403', 'Balvenie Caribbean Cask 14-Year is so unique. The rum cask finish adds a sweet twist. What are your favorite cask finishes?', '{}', 1),
    (1, '2024-11-12 19:40:31.403', 'Just opened a bottle of Bunnahabhain 12-Year. It’s unpeated but still full of character. A great alternative to Islay smoke.', '{}', 2),
    (1, '2024-11-13 20:10:31.403', 'Who’s tried Japanese whiskies like Hibiki or Nikka? I’m amazed at how refined they are!', '{}', 3),
    (1, '2024-11-14 17:45:31.403', 'Eagle Rare 10-Year is my pick for the night. Great balance of caramel, vanilla, and oak. What’s your favorite bourbon?', '{}', 4),
    (1, '2024-11-15 19:50:31.403', 'Tried a whisky-infused chocolate today. It was divine! Anyone else into whisky pairings?', '{}', 1),
    (1, '2024-11-16 21:15:31.403', 'Lagavulin 16-Year is perfection in a bottle. Smoky, rich, and complex. Can’t wait to try the 12-Year soon.', '{}', 2),
    (1, '2024-11-17 18:30:31.403', 'Sampled Glenkinchie 12-Year. A very light and floral Lowland whisky. Perfect for a sunny day.', '{}', 3),
    (1, '2024-11-18 19:25:31.403', 'Anyone else a fan of blended whiskies? I just had Johnnie Walker Green Label, and it’s fantastic.', '{}', 4),
    (1, '2024-11-19 20:45:31.403', 'Exploring rye whiskies lately. Had Knob Creek Rye tonight, and it’s spicy and bold! Any other ryes to recommend?', '{}', 1),
    (1, '2024-11-20 21:30:31.403', 'Whisky fact: Did you know Scotch legally needs to be aged in oak barrels for at least 3 years? Learned this at a tour!', '{}', 2),
    (1, '2024-11-21 18:20:31.403', 'Opened a Glen Grant 10-Year. Light, fruity, and perfect for casual sipping. What’s your everyday whisky?', '{}', 3),
    (1, '2024-11-22 19:15:31.403', 'Received a bottle of Dalmore 12-Year as a gift. It’s elegant and rich. Anyone tried the King Alexander III?', '{}', 4),
    (1, '2024-11-23 20:40:31.403', 'Experimented with whisky and coffee tonight. A splash of Jameson made it amazing. What’s your favorite whisky-based drink?', '{}', 3),
    (1, '2024-11-24 21:50:31.403', 'Visited Scotland last year and toured Glenmorangie. Their 18-Year is unforgettable. Who else has done a distillery tour?', '{}', 1),
    (1, '2024-11-25 18:35:31.403', 'Decided to try something new—peated Irish whisky! Connemara was a pleasant surprise.', '{}', 2),
    (1, '2024-11-26 19:20:31.403', 'Found a local store selling rare whiskies. Picked up a Springbank 15-Year. Can’t wait to try it!', '{}', 3),
    (1, '2024-11-27 20:55:31.403', 'Looking for recommendations: What’s a good budget-friendly whisky for everyday sipping?', '{}', 1),
    (1, '2024-11-28 21:45:31.403', 'Whisky trivia: Did you know that bourbon must be made in the U.S. and use at least 51% corn? Cheers to learning!', '{}', 2),
    (1, '2024-11-29 18:25:31.403', 'GlenDronach 12-Year is a hidden gem. Rich, sherry-forward, and affordable. Highly recommend it!', '{"https://m.media-amazon.com/images/I/710obA9RM7L._AC_UF1000,1000_QL80_.jpg", "https://maltwineasia.com/wp-content/uploads/2024/08/The-Glendronach-Original-12-Years-New.jpg", "https://maltwineasia.com/wp-content/uploads/2024/08/The-Glendronach-Original-12-Years-New-Banner-1300x650.jpg"}', 3);

INSERT INTO "clubPostsLikes"(
    "clubID", "postID", "memberID")
VALUES
    (1, 1, 2),
    (1, 1, 3);

INSERT INTO "clubPostComments"(
    "postID", "commentDate", "commentContent", "commenterID")
VALUES
    (1, '2024-11-01 18:45:31.403', 'I usually enjoy it neat as well. Sometimes I add a drop or 2 of water to open up the flavors even more.\n\nFor your next try, I''d recommend Hakushu 12 if you want something lighter and herbal.', 2),
    (1, '2024-11-01 19:00:31.403', 'I always go neat with Yamazaki! If you''re into Japanese whisky, try Nikka From The Barrel—it''s incredible.', 3),
    (1, '2024-11-01 19:10:31.403', 'Adding a splash of water can really open up those fruity notes. Hakushu 12 is a great next step!', 1),
    (1, '2024-11-01 19:20:31.403', 'I like Yamazaki with a single large ice cube—keeps it cool without diluting too fast. For your next try, maybe go for Hibiki Harmony.', 2),
    (1, '2024-11-01 19:30:31.403', 'Yamazaki 12 is a classic! Try Glenlivet 18 for something equally smooth but a bit more robust.', 3),
    (1, '2024-11-01 19:40:31.403', 'Neat is the way to go! If you enjoy this, you might like Balvenie DoubleWood 12.', 1),
    (1, '2024-11-01 19:50:31.403', 'I prefer mine with just a couple of drops of water to release the aromas. You should try Kavalan Solist Sherry Cask next.', 2),
    (1, '2024-11-01 20:00:31.403', 'I usually go for it neat as well, but pairing it with dark chocolate really enhances the flavors.', 3),
    (1, '2024-11-01 20:10:31.403', 'Try Glenmorangie Signet if you''re looking for something bold and rich. It’s one of my favorites!', 1),
    (1, '2024-11-01 20:20:31.403', 'I''ve heard adding a bit of chilled green tea to Yamazaki is popular in Japan. Ever tried that?', 2),
    (1, '2024-11-01 20:30:31.403', 'I love Yamazaki! I think the Nikka Yoichi 10-Year would be a great follow-up for something smokier.', 3),
    (1, '2024-11-01 20:40:31.403', 'Neat or on the rocks, Yamazaki never disappoints. Next on your list should be Dalmore 15.', 1),
    (1, '2024-11-01 20:50:31.403', 'I''d recommend trying Glenfiddich 18 for a similar smoothness with a bit more spice.', 2),
    (1, '2024-11-01 21:00:31.403', 'Adding a few drops of water always works for me. As for recommendations, try Suntory''s Toki—it''s lighter but still fantastic.', 3),
    (1, '2024-11-01 21:10:31.403', 'Yamazaki is best enjoyed neat! For your next try, GlenDronach 12 is an excellent sherried option.', 4),
    (1, '2024-11-01 21:20:31.403', 'I''ve found that Yamazaki pairs surprisingly well with a mild cigar. Ever tried pairing whisky with cigars?', 2),
    (1, '2024-11-01 21:30:31.403', 'I suggest experimenting with small sips after warming the glass in your hands. Also, try Macallan 12 next!', 3),
    (1, '2024-11-01 21:40:31.403', 'Neat is my go-to as well! If you’re looking for something a bit peaty, try Laphroaig Quarter Cask.', 1),
    (1, '2024-11-01 21:50:31.403', 'I love how Yamazaki evolves over time in the glass. For your next bottle, I''d recommend Oban 14.', 2),
    (1, '2024-11-01 22:00:31.403', 'Yamazaki is a solid choice! Next, consider trying Compass Box Hedonism for a unique experience.', 4),
    (1, '2024-11-01 22:10:31.403', 'I find that Yamazaki is perfect for slow evenings. Try Glenkinchie 12 next for something light and floral.', 1),
    (1, '2024-11-01 22:20:31.403', 'Adding a touch of honey really enhances the sweet notes for me. Next, give Aberlour A’bunadh a shot.', 2),
    (1, '2024-11-01 22:30:31.403', 'Yamazaki is a favorite of mine! If you like it, you might enjoy Auchentoshan Three Wood.', 3),
    (1, '2024-11-01 22:40:31.403', 'Drinking it neat really lets the complexity shine. I think Glenfarclas 15-Year could be your next favorite.', 1),
    (1, '2024-11-01 22:50:31.403', 'I’d suggest pairing it with a cheese platter—it''s amazing! Next, try Balblair 15-Year.', 2),
    (1, '2024-11-01 23:00:31.403', 'I love Yamazaki 12! If you’re feeling adventurous, go for Ardbeg An Oa—it''s very different but delightful.', 3),
    (1, '2024-11-01 23:10:31.403', 'Try a few sips while eating roasted almonds or dried fruits—it really complements the flavors.', 1),
    (1, '2024-11-01 23:20:31.403', 'Neat is the only way for Yamazaki. I''d suggest Highland Park 18-Year for your next exploration.', 1),
    (1, '2024-11-01 23:30:31.403', 'I always drink it neat, but on a hot day, a splash of soda water works well. Try Hibiki 17-Year next!', 2),
    (1, '2024-11-01 23:40:31.403', 'Yamazaki is best savored slowly. I think Redbreast 12-Year is a great one to explore next.', 3);

INSERT INTO "clubPostCommentsLikes"(
    "postID", "commentID", "memberID")
VALUES
    (1, 1, 3);