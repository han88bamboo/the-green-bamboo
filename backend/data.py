# Imported file for MongoDB dataclasses

from dataclasses import dataclass, asdict
from typing import Optional, Union
import pymongo
import json
from datetime import datetime


from dotenv import load_dotenv
import os

# Connect to MongoDB
client = pymongo.MongoClient(os.getenv('MONGO_DB_URL'))
database = client["DrinkX"]

# collection = database['your_collection']

#NOTE TO DEVELOPERS, TO INSERT DATA INTO MONGO, CREATE A DATA INSTANCE OF THE DATACLASS NEEDED, THEN USE 
# asdict(data) TO INSERT INTO MONGO

# ========= TO BE DELETED =========
# 1. drinkTypesOld
# 2. listingsBackup
# 3. listingsCopy
# 4. listingsOld
# 5. producersOld
# 6. testImport
# 7. testImport2
# 8. venuesAPI
# 9. venuesOld
# ===================================

# ========= accountRequests =========
@dataclass
class accountRequests:
    businessName: str
    businessType: str
    businessDesc: str
    country: str
    pricing: str
    businessLink: str
    firstName: str
    lastName: str
    email: str
    relationship: str
    photo: str
    joinDate: datetime
    reviewStatus: bool

# ========= badges =========
@dataclass
class badges:
    badgeName: str
    badgePhoto: str
    badgeDesc: str

# ========= colours =========
@dataclass
class colours:
    hexcode: str

# ========= countries =========
@dataclass
class countries:
    originCountry: str
    legalAge: int

# ========= drinkTypes =========
@dataclass
class drinkTypes:
    drinkType: str
    badgePhoto: str
    typeCategory: Optional[list] = None

# ========= flavourTags =========
@dataclass
class flavourTags:
    hexcode: str
    familyTag: str

# ========= languages =========
@dataclass
class languages:
    language: str

# ========= listings =========
@dataclass
class listings:
    listingName: str
    producerID: object
    bottler: str
    originCountry: str
    drinkType: str
    abv: float
    officialDesc: str
    allowMod: bool
    addedDate: datetime
    typeCategory: Optional[str] = None
    age: Optional[str] = None
    reviewLink: Optional[str] = None
    sourceLink: Optional[str] = None
    photo: Optional[str] = None

# ========= modRequests =========
@dataclass
class modRequests:
    userID: object
    drinkType: str
    modDesc: str
    reviewStatus: bool

# ========= observationTags =========
@dataclass
class observationTags:
    observationTag: str

# ========= producers =========
@dataclass
class producers:
    producerName: str
    producerDesc: str
    originCountry: str
    mainDrinks: list
    photo: str
    hashedPassword: str
    hashedPassword:str
    claimStatus: bool
    statusOB: Optional[str] = None
    questionAnswers: Optional[list] = None
    updates: Optional[list] = None
    producerLink: Optional[str] = None

# ========= producersProfileViews =========
@dataclass
class producersProfileViews:
    producerID: object
    views: Optional[list] = None

# ========= requestEdits =========
@dataclass
class requestEdits:
    editDesc: str
    listingID: object
    userID: object
    brandRelation: str
    reviewStatus: bool
    duplicateLink: Optional[str] = None
    sourceLink: Optional[str] = None

# ========= requestInaccuracy =========
@dataclass
class requestInaccuracy:
    listingID: object
    userID: object
    venueID: object
    reportDate: datetime
    inaccurateReason: Optional[str] = None
    reviewStatus: Optional[bool] = False

# ========= requestListings =========
@dataclass
class requestListings:
    listingName: str
    bottler: str
    drinkType: str
    sourceLink: str
    brandRelation: str
    reviewStatus: bool
    userID: object
    photo: str
    originCountry: Optional[str] = None
    producerID: Optional[object] = None
    producerNew: Optional[str] = None
    typeCategory: Optional[str] = None
    abv: Optional[str] = None
    age: Optional[str] = None
    reviewLink: Optional[str] = None

# ========= reviews =========
@dataclass
class reviews:
    userID: object
    reviewTarget: object
    rating: int
    reviewDesc: str
    reviewType: str
    createdDate: datetime
    language: str
    finish: str
    willRecommend: bool
    wouldBuyAgain: bool
    userVotes: object
    taggedUsers: Optional[list] = None
    flavorTag: Optional[list] = None
    photo: Optional[str] = None
    colour: Optional[str] = None
    aroma: Optional[str] = None
    location: Optional[object] = None
    taste: Optional[str] = None
    observationTag: Optional[list] = None
    address: Optional[str] = None

# ========= servingTypes =========
@dataclass
class servingTypes:
    servingType: str

# ========= specialColours =========
@dataclass
class specialColours:
    hexList: list
    colour: str

# ========= subTags =========
@dataclass
class subTags:
    familyTagId: object
    subTag: str

# ========= users =========
@dataclass
class users:
    username: str
    displayName: str
    choiceDrinks: list
    modType: list
    photo: str
    hashedPassword: str
    drinkLists: object
    joinDate: datetime
    followLists: object
    firstName: str
    lastName: str
    email: str
    isAdmin: bool
    birthday: datetime

# ========= venues =========
@dataclass
class venues:
    venueName: str
    address: str
    venueType: str
    originLocation: str
    venueDesc: str
    menu: list
    hashedPassword: str
    photo: str
    claimStatus: bool
    openingHours: object
    questionAnswers: Optional[list] = None
    updates: Optional[list] = None
    reservationDetails: Optional[str] = None
    publicHolidays: Optional[str] = None

# ========= venuesProfileViews =========
@dataclass
class venuesProfileViews:
    venueID: object
    views: Optional[list] = None

def convert_to_json(data):
    return json.dumps(data.__dict__)