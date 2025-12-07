import os
from flask import Blueprint, request, jsonify, g
from psycopg2.extras import RealDictCursor
import psycopg2
from datetime import datetime
from decimal import Decimal, InvalidOperation
import pandas as pd
import io
import re
import unicodedata
from fuzzywuzzy import fuzz

# Import the database manager for connection pooling
from app import db_manager

# Import username utilities
from scripts.username_utils import generate_unique_username

file_name = os.path.basename(__file__)
blueprint = Blueprint(file_name[:-3], __name__)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def sanitize_username(producer_name):
    """
    Sanitize producer name for use as username by:
    1. Removing Chinese/Japanese characters (CJK ideographs)
    2. Removing accented characters (converting to ASCII equivalents)
    3. Removing special characters including spaces (keep only alphanumeric, hyphens, underscores)
    4. Converting to lowercase for consistency
    5. Stripping leading/trailing whitespace
    
    WARNING: If the producer name contains ONLY Chinese/Japanese characters with no English letters
    (e.g., "山崎蒸留所"), the result will be the original unsanitized producer name. This means
    the username may contain special characters that could cause issues with authentication
    or URL handling.
    """
    print(f"DEBUG: Input producer_name: '{producer_name}' (type: {type(producer_name)})")
    
    if not producer_name:
        return ""
    
    # Step 1: Remove CJK (Chinese, Japanese, Korean) characters
    # Unicode ranges for CJK characters:
    # U+4E00-U+9FFF: CJK Unified Ideographs
    # U+3400-U+4DBF: CJK Extension A
    # U+20000-U+2A6DF: CJK Extension B
    # U+3040-U+309F: Hiragana
    # U+30A0-U+30FF: Katakana
    cjk_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff]+')
    cleaned_name = cjk_pattern.sub('', producer_name)
    print(f"DEBUG: After CJK removal: '{cleaned_name}'")
    
    # Step 2: Convert accented characters to ASCII equivalents (NFD normalization)
    # This converts characters like Ā, Å, é, ñ to their base ASCII forms
    normalized = unicodedata.normalize('NFD', cleaned_name)
    ascii_name = ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')
    print(f"DEBUG: After ASCII conversion: '{ascii_name}'")
    
    # Step 3: Remove any remaining non-ASCII characters and special characters including spaces
    # Keep only alphanumeric, hyphens, and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '', ascii_name)
    print(f"DEBUG: After special char and space removal: '{sanitized}'")
    
    # Step 4: Convert to lowercase for consistency
    sanitized = sanitized.lower()
    print(f"DEBUG: After lowercase conversion: '{sanitized}'")
    
    # Step 5: If the result is empty (all characters were removed), use original producer name
    if not sanitized:
        print(f"DEBUG: Result was empty, returning original: '{producer_name}'")
        return producer_name
    
    print(f"DEBUG: Final result: '{sanitized}'")
    return sanitized

def hash_password(id, password):
    combinedString = str(id) + password
    hash = 0
    for i in range(len(combinedString)):
        char = ord(combinedString[i])
        hash = (hash << 5) - hash + char
        hash &= 0xFFFFFFFF
    if hash & (1 << 31):
        hash -= 1 << 32
    return hash

def get_normalize_sql():
    """Returns SQL function to normalize text for comparison"""
    return """
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                LOWER(
                    TRANSLATE(
                        {field},
                        'áàâäãåāăąÁÀÂÄÃÅĀĂĄéèêëēėęÉÈÊËĒĖĘíìîïīįÍÌÎÏĪĮóòôöõøōőÓÒÔÖÕØŌŐúùûüūůűÚÙÛÜŪŮŰçćčĆČñńÑŃ',
                        'aaaaaaaaaaaaaaaaaeeeeeeeeeeeeeeiiiiiiiiiiiioooooooooooooooouuuuuuuuuuuuuuccccnnnn'
                    )
                ),
                '[^a-z0-9\s]', '', 'g'
            ),
            '\s+', ' ', 'g'
        )
    """

def normalize_string(s):
    """
    Normalize string for better matching:
    - Convert to lowercase
    - Remove accents (Ã -> A, é -> e)
    - Remove special characters (except letters, numbers, spaces)
    - Trim whitespace
    """
    if not s:
        return ""
    
    # Normalize unicode characters and remove accents
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ASCII', 'ignore').decode('ASCII')
    
    # Convert to lowercase
    s = s.lower()
    
    # Remove special characters except spaces and numbers
    s = re.sub(r'[^a-z0-9\s]', '', s)
    
    # Remove extra whitespace
    s = ' '.join(s.split())
    
    return s

def normalize_db_string_sql():
    """
    Returns SQL expression to normalize a database column the same way as normalize_string()
    """
    # This creates an SQL expression that does the same normalization as Python
    return """
        LOWER(
            regexp_replace(
                translate(
                    unaccent({column}),
                    'àâäæçéèêëîïôœùûüÿ',
                    'aaaaceeeeiioouuuy'
                ),
                '[^a-z0-9 ]', '', 'g'
            )
        )
    """

def parse_date(date_str):
    """Parse date from various formats"""
    if not date_str or pd.isna(date_str):
        return None
    
    # Convert to string and strip whitespace
    date_str = str(date_str).strip()
    if not date_str or date_str.lower() in ['', 'nan', 'none', 'null']:
        return None
    
    formats = [
        # Common numeric formats (try these first for performance)
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%y',
        '%m/%d/%y',
        '%Y%m%d',
        # Month name formats (for human-readable dates)
        '%d %B %Y',        # "04 June 2020" (full month name)
        '%d %b %Y',        # "04 Jun 2020" (abbreviated month)
        '%B %d, %Y',       # "June 04, 2020" 
        '%b %d, %Y',       # "Jun 04, 2020"
        '%d-%B-%Y',        # "04-June-2020"
        '%d-%b-%Y',        # "04-Jun-2020"
        '%Y %B %d',        # "2020 June 04"
        '%Y %b %d',        # "2020 Jun 04"
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt).date()
            # Sanity check: year should be reasonable (1900-2100)
            if 1900 <= parsed_date.year <= 2100:
                return parsed_date
        except (ValueError, TypeError):
            continue
    
    print(f"Could not parse date: {date_str}")
    return None

def parse_decimal(value):
    """Parse decimal from various formats"""
    if not value or pd.isna(value):
        return None
    
    try:
        # Convert to string and clean
        clean_value = str(value).strip()
        if not clean_value or clean_value.lower() in ['', 'nan', 'none', 'null']:
            return None
        
        # Remove currency symbols, commas, and other non-numeric chars (except . and -)
        clean_value = re.sub(r'[^\d.-]', '', clean_value)
        
        if not clean_value or clean_value == '-':
            return None
            
        result = Decimal(clean_value)
        return result if result >= 0 else None
    except (InvalidOperation, TypeError, ValueError):
        return None

def parse_integer(value):
    """Parse integer from various formats"""
    if not value or pd.isna(value):
        return None
    
    try:
        # Convert to string and clean
        clean_value = str(value).strip()
        if not clean_value or clean_value.lower() in ['', 'nan', 'none', 'null']:
            return None
        
        # Remove any non-digit characters
        clean_value = re.sub(r'[^\d]', '', clean_value)
        
        if not clean_value:
            return None
            
        result = int(clean_value)
        return result if result > 0 else None
    except (ValueError, TypeError):
        return None

def validate_import_row(row, required_fields=None):
    """Validate a single import row"""
    if required_fields is None:
        required_fields = ['listingName']
    
    errors = []
    
    for field in required_fields:
        if not row.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate field constraints
    if 'status' in row and row['status']:
        valid_statuses = ['In Possession', 'On Its Way', 'Purchased', 'Held Elsewhere', 'Wishlisted', 'Consumed']
        if row['status'] not in valid_statuses:
            errors.append(f"Invalid status: {row['status']}. Must be one of: {', '.join(valid_statuses)}")
    
    if 'consumption' in row and row['consumption']:
        valid_consumption = ['Opened', 'Unopened', 'Empty']
        if row['consumption'] not in valid_consumption:
            errors.append(f"Invalid consumption: {row['consumption']}. Must be one of: {', '.join(valid_consumption)}")
    
    return errors

# ============================================================================
# STEP 1: PARSE CSV AND RETURN PREVIEW
# ============================================================================

@blueprint.route("/parseCsvPreview", methods=['POST'])
def parseCsvPreview():
    """Parse uploaded CSV and return headers + sample rows for column mapping"""
    print("parseCsvPreview called")
    
    try:
        if 'file' not in request.files:
            return jsonify({"code": 400, "message": "No file uploaded"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"code": 400, "message": "No file selected"}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({"code": 400, "message": "File must be a CSV"}), 400
        
        # Read file content as bytes
        file_content = file.stream.read()
        
        # Try multiple encodings
        encodings_to_try = [
            'utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 
            'iso-8859-1', 'utf-16', 'utf-16le', 'utf-16be'
        ]
        
        decoded_content = None
        successful_encoding = None
        
        for encoding in encodings_to_try:
            try:
                decoded_content = file_content.decode(encoding)
                successful_encoding = encoding
                print(f"Successfully decoded with encoding: {encoding}")
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if decoded_content is None:
            try:
                decoded_content = file_content.decode('utf-8', errors='replace')
                successful_encoding = 'utf-8 (with replacements)'
            except Exception as e:
                return jsonify({
                    "code": 400,
                    "message": f"Unable to decode CSV file. Error: {str(e)}"
                }), 400
        
        # Create StringIO from decoded content
        stream = io.StringIO(decoded_content)
        
        # Read CSV with pandas
        try:
            df = pd.read_csv(stream)
        except pd.errors.ParserError:
            stream.seek(0)
            try:
                df = pd.read_csv(stream, sep=None, engine='python', on_bad_lines='skip')
            except Exception as e:
                return jsonify({
                    "code": 400,
                    "message": f"Error parsing CSV structure: {str(e)}"
                }), 400
        
        # Clean headers - remove BOM and special characters
        headers = [str(h).strip().replace('\ufeff', '').replace('\u200b', '') for h in df.columns]
        df.columns = headers
        
        # Get sample data
        sample_data = df.head(10).fillna('').to_dict('records')
        total_rows = len(df)
        
        print(f"Parsed CSV with {len(headers)} columns and {total_rows} rows")
        
        return jsonify({
            "code": 200,
            "message": f"CSV parsed successfully (encoding: {successful_encoding})",
            "data": {
                "headers": headers,
                "sampleData": sample_data,
                "totalRows": total_rows,
                "encoding": successful_encoding
            }
        }), 200
        
    except Exception as e:
        print(f"Error parsing CSV: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "code": 500,
            "message": f"Error parsing CSV: {str(e)}"
        }), 500

# ============================================================================
# STEP 2: PROCESS MAPPED CSV AND DETECT DUPLICATES
# ============================================================================

@blueprint.route("/processAndDetectDuplicates", methods=['POST'])
def processAndDetectDuplicates():
    """
    Process CSV with column mappings and detect potential duplicate drinks
    """
    print("processAndDetectDuplicates called")
    
    try:
        if 'file' not in request.files:
            return jsonify({"code": 400, "message": "No file uploaded"}), 400
        
        file = request.files['file']
        column_mapping_json = request.form.get('columnMapping')
        threshold = int(request.form.get('threshold', 85))
        
        if not column_mapping_json:
            return jsonify({"code": 400, "message": "Column mapping is required"}), 400
        
        import json
        column_mapping = json.loads(column_mapping_json)

        # Check for duplicate mappings
        db_field_usage = {}
        for csv_col, db_field in column_mapping.items():
            if db_field and db_field.strip():
                if db_field not in db_field_usage:
                    db_field_usage[db_field] = []
                db_field_usage[db_field].append(csv_col)

        duplicate_fields = {k: v for k, v in db_field_usage.items() if len(v) > 1}
        if duplicate_fields:
            error_msg = "Duplicate column mappings detected: " + ", ".join(
                [f"{field} mapped from {', '.join(cols)}" for field, cols in duplicate_fields.items()]
            )
            return jsonify({
                "code": 400,
                "message": error_msg
            }), 400
        
        # Read and decode file
        file_content = file.stream.read()
        encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        
        decoded_content = None
        for encoding in encodings_to_try:
            try:
                decoded_content = file_content.decode(encoding)
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if decoded_content is None:
            decoded_content = file_content.decode('utf-8', errors='replace')
        
        # Parse CSV
        stream = io.StringIO(decoded_content)
        try:
            df = pd.read_csv(stream)
        except pd.errors.ParserError:
            stream.seek(0)
            df = pd.read_csv(stream, sep=None, engine='python', on_bad_lines='skip')
        
        # Clean headers
        df.columns = [str(h).strip().replace('\ufeff', '').replace('\u200b', '') for h in df.columns]
        
        # Check if unaccent extension is available
        try:
            with db_manager.get_cursor() as cursor:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
                has_unaccent = True
                print("unaccent extension available")
        except Exception as e:
            print(f"Could not enable unaccent extension: {e}")
            has_unaccent = False
        
        results = []
        
        # Use a single database connection for all duplicate searches
        with db_manager.get_cursor() as cursor:
            for index, row in df.iterrows():
                # Map CSV columns to database fields
                mapped_data = {}
                for csv_column, db_field in column_mapping.items():
                    if db_field and csv_column in row:
                        value = row[csv_column]
                        # Skip empty values
                        if pd.isna(value) or str(value).strip() == '':
                            continue
                        
                        # Type conversion based on field
                        if db_field in ['purchaseDate', 'deliveryDate', 'drinkOnwardsDate', 'drinkByDate']:
                            parsed = parse_date(value)
                            if parsed:
                                mapped_data[db_field] = parsed
                        elif db_field in ['purchasePrice', 'currentValueEstimation', 'abv']:
                            parsed = parse_decimal(value)
                            if parsed:
                                mapped_data[db_field] = float(parsed) if db_field == 'abv' else parsed
                        elif db_field in ['variant', 'quantity']:
                            parsed = parse_integer(value)
                            if parsed:
                                mapped_data[db_field] = parsed
                        elif db_field == 'volumeNumber':
                            parsed = parse_decimal(value)
                            if parsed:
                                mapped_data[db_field] = parsed
                        else:
                            mapped_data[db_field] = str(value).strip()
                
                # Validate required fields
                validation_errors = validate_import_row(mapped_data)
                if validation_errors:
                    results.append({
                        "rowNumber": index + 2,  # +2 because CSV is 1-indexed and has header row
                        "mappedData": mapped_data,
                        "possibleMatches": [],
                        "validationErrors": validation_errors
                    })
                    continue
                
                # Search for potential duplicate drinks
                drink_name = mapped_data.get('listingName', '').strip()
                producer_name = mapped_data.get('producerName', '').strip()
                variant = mapped_data.get('variant')
                
                if not drink_name:
                    results.append({
                        "rowNumber": index + 2,
                        "mappedData": mapped_data,
                        "possibleMatches": [],
                        "validationErrors": ["Drink name is required"]
                    })
                    continue
                
                # Normalize the search term
                normalized_name = normalize_string(drink_name)
                normalized_producer = normalize_string(producer_name) if producer_name else None

                print(f"Searching for: {drink_name} (normalized: {normalized_name})")

                # Build search query with proper normalization
                normalize_listing = get_normalize_sql().format(field='l."listingName"')
                normalize_producer_sql = get_normalize_sql().format(field='p."producerName"')

                search_query = f"""
                    SELECT 
                        l."id",
                        l."listingName",
                        l."producerID",
                        p."producerName",
                        l."drinkType",
                        l."originCountry",
                        l."abv",
                        l."photo"
                    FROM "listings" l
                    LEFT JOIN "producers" p ON l."producerID" = p."id"
                    WHERE {normalize_listing} LIKE %s
                """

                search_params = [f'%{normalized_name}%']

                # Add producer filter if available
                if normalized_producer:
                    search_query += f" OR {normalize_producer_sql} LIKE %s"
                    search_params.append(f'%{normalized_producer}%')

                search_query += " LIMIT 20"
                
                try:
                    cursor.execute(search_query, search_params)
                    potential_matches = cursor.fetchall()
                    print(f"Found {len(potential_matches)} potential matches from database")
                except Exception as e:
                    print(f"Error searching for matches: {e}")
                    import traceback
                    print(traceback.format_exc())
                    results.append({
                        "rowNumber": index + 2,
                        "mappedData": mapped_data,
                        "possibleMatches": [],
                        "validationErrors": []
                    })
                    continue
                
                # Calculate fuzzy match scores
                matches_with_scores = []
                for match in potential_matches:
                    try:
                        # Normalize both strings for comparison
                        match_name_normalized = normalize_string(match['listingName'])
                        match_producer_normalized = normalize_string(match['producerName']) if match['producerName'] else ''
                        
                        # Name similarity (primary factor) - using normalized strings
                        name_score = fuzz.ratio(normalized_name, match_name_normalized)
                        
                        # Producer match bonus
                        producer_bonus = 0
                        if normalized_producer and match_producer_normalized:
                            producer_score = fuzz.ratio(normalized_producer, match_producer_normalized)
                            if producer_score >= 90:
                                producer_bonus = 20  # Increased bonus for exact producer match
                            elif producer_score >= 80:
                                producer_bonus = 15
                            elif producer_score >= 60:
                                producer_bonus = 10
                        
                        # Variant match bonus
                        variant_bonus = 0
                        if variant and match.get('variant'):
                            # Exact variant match
                            if str(variant) == str(match['variant']):
                                variant_bonus = 15  # Increased bonus for exact variant match
                            # Close variant match (within 1 year for vintages)
                            elif abs(int(variant) - int(match['variant'])) <= 1:
                                variant_bonus = 5
                        elif variant and not match.get('variant'):
                            # CSV has variant but DB doesn't - slight penalty
                            variant_bonus = -5
                        elif not variant and match.get('variant'):
                            # CSV doesn't have variant but DB does - slight penalty
                            variant_bonus = -5
                        
                        # Calculate total score
                        total_score = min(100, name_score + producer_bonus + variant_bonus)
                        
                        print(f"Match '{match['listingName']}' - Name:{name_score}, Producer:{producer_bonus}, Variant:{variant_bonus}, Total:{total_score}")
                        
                        if total_score >= threshold:
                            matches_with_scores.append({
                                "id": match['id'],
                                "listingName": match['listingName'],
                                "producerName": match['producerName'],
                                "variant": match.get('variant'),
                                "drinkType": match['drinkType'],
                                "originCountry": match['originCountry'],
                                "abv": float(match['abv']) if match['abv'] else None,
                                "photo": match['photo'],
                                "similarity": round(total_score, 1)
                            })
                    except Exception as e:
                        print(f"Error calculating match score: {e}")
                        continue
                
                # Sort by similarity score (highest first)
                matches_with_scores.sort(key=lambda x: x['similarity'], reverse=True)
                
                print(f"Row {index + 2} - {len(matches_with_scores)} matches above threshold")
                
                results.append({
                    "rowNumber": index + 2,
                    "mappedData": mapped_data,
                    "possibleMatches": matches_with_scores[:10],  # Top 10 matches
                    "validationErrors": []
                })
        
        print(f"Processed {len(results)} rows successfully")
        
        return jsonify({
            "code": 200,
            "message": f"Processed {len(results)} rows",
            "data": {
                "items": results,
                "totalRows": len(results)
            }
        }), 200
        
    except Exception as e:
        print(f"Error in processAndDetectDuplicates: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "code": 500,
            "message": f"Error processing CSV: {str(e)}"
        }), 500

# ============================================================================
# STEP 3: IMPORT TO CELLAR WITH USER DECISIONS
# ============================================================================

def create_new_listing(cur, mapped_data, owner_type, owner_id):
    listing_name = mapped_data.get('listingName')
    producer_name = mapped_data.get('producerName')
    drink_type = mapped_data.get('drinkType', 'Other')
    origin_country = mapped_data.get('originCountry')
    type_category = mapped_data.get('typeCategory')
    abv = mapped_data.get('abv')
    
    # Find or create producer
    producer_id = None
    if producer_name:
        # Try to find existing producer (case-insensitive, normalized)
        try:
            cur.execute("""
                SELECT "id", "producerName" FROM "producers" 
                WHERE LOWER(regexp_replace(unaccent("producerName"), '[^a-z0-9 ]', '', 'g')) 
                = LOWER(regexp_replace(unaccent(%s), '[^a-z0-9 ]', '', 'g'))
                LIMIT 1
            """, (producer_name,))
            producer = cur.fetchone()
        except Exception as e:
            # Fallback if unaccent extension not available
            print(f"Unaccent query failed, using simple LOWER: {e}")
            cur.execute("""
                SELECT "id", "producerName" FROM "producers" 
                WHERE LOWER("producerName") = LOWER(%s)
                LIMIT 1
            """, (producer_name,))
            producer = cur.fetchone()
        
        if producer:
            producer_id = producer['id']
            print(f"Found existing producer: {producer['producerName']} (ID: {producer_id})")
        else:
            # Create new producer with unique username
            print(f"Creating new producer: {producer_name}")
            
            # First sanitize the producer name, then ensure uniqueness
            sanitized_username = sanitize_username(producer_name)
            if not sanitized_username:
                sanitized_username = "producer"  # Fallback for empty sanitization result
            
            unique_username = generate_unique_username(sanitized_username, cur)
            print(f"Generated unique username: {unique_username}")
            
            cur.execute("""
                INSERT INTO "producers" (
                    "producerName", "producerDesc", "originCountry", "mainDrinks",
                    "photo", "hashedPassword", "claimStatus", "statusOB", 
                    "username", "producerLink", "stripeCustomerId", "isIndependentBottler"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "id"
            """, (
                producer_name, "", origin_country or "", [],
                "", hash_password(unique_username, "admin1234"), False, "",
                unique_username, "", None, False
            ))
            producer_id = cur.fetchone()['id']
            print(f"Created new producer with ID: {producer_id} and username: {unique_username}")
    
    # === STEP 1: Record in requestListings for tracking ===
    # Determine user/venue ID based on owner type
    user_id = None
    venue_id = None
    submitter_type = owner_type  # 'user', 'producer', or 'venue'
    
    if owner_type == 'user':
        user_id = owner_id
    elif owner_type == 'venue':
        venue_id = owner_id
    
    # Convert abv to string for requestListings (table expects VARCHAR)
    abv_str = str(abv) if abv is not None else None
    
    print(f"Recording in requestListings - submitter: {submitter_type} #{owner_id}")
    
    cur.execute("""
        INSERT INTO "requestListings" (
            "listingName",
            "producerID",
            "producerNew",
            "drinkType",
            "originCountry",
            "typeCategory",
            "abv",
            "userID",
            "venueID",
            "submitterType",
            "reviewStatus",
            "sourceLink"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING "id"
    """, (
        listing_name,
        producer_id,
        producer_name if not producer_id else None,  # Store producer name if new
        drink_type,
        origin_country,
        type_category,
        abv_str,
        user_id,
        venue_id,
        submitter_type,
        True,  # reviewStatus = True (auto-approved from CSV import)
        'CSV_CELLAR_IMPORT'  # Special marker to identify CSV imports
    ))
    
    request_listing_id = cur.fetchone()['id']
    print(f"Recorded in requestListings with ID: {request_listing_id}")
    
    # === STEP 2: Create the actual listing ===
    cur.execute("""
        INSERT INTO "listings" (
            "listingName", 
            "producerID", 
            "originCountry", 
            "drinkType",
            "typeCategory", 
            "abv", 
            "addedDate", 
            "allowMod"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING "id"
    """, (
        listing_name, 
        producer_id, 
        origin_country, 
        drink_type,
        type_category, 
        abv, 
        datetime.now(), 
        True
    ))
    
    new_listing_id = cur.fetchone()['id']
    print(f"Created new listing: '{listing_name}' with ID: {new_listing_id}")
    
    return new_listing_id

def add_cellar_item_from_import(cellar_data):
    """Add item to cellar with proper duplicate handling"""
    with db_manager.get_cursor() as cursor:
        listing_id = cellar_data['listingId']
        owner_type = cellar_data['ownerType']
        owner_id = cellar_data['ownerId']
        collection_id = cellar_data['collectionId']
        quantity = cellar_data.get('quantity', 1)
        
        # Ensure quantity is at least 1
        if quantity < 1:
            quantity = 1
        
        # Group properties
        variant = cellar_data.get('variant')
        format_value = cellar_data.get('format', 'Bottle')
        volume_number = cellar_data.get('volumeNumber', 750)
        volume_unit = cellar_data.get('volumeUnit', 'ml')
        drink_onwards_date = cellar_data.get('drinkOnwardsDate')
        drink_by_date = cellar_data.get('drinkByDate')
        current_value_estimation = cellar_data.get('currentValueEstimation')
        current_value_currency = cellar_data.get('currentValueCurrency', 'USD')
        suggested_food_pairing = cellar_data.get('suggestedFoodPairing')
        
        # Individual properties
        purchase_date = cellar_data.get('purchaseDate')
        delivery_date = cellar_data.get('deliveryDate')
        purchase_price = cellar_data.get('purchasePrice')
        purchase_currency = cellar_data.get('purchaseCurrency', 'USD')
        purchase_place_name = cellar_data.get('purchasePlaceName')
        purchase_address = cellar_data.get('purchaseAddress')
        status = cellar_data.get('status', 'In Possession')
        consumption = cellar_data.get('consumption', 'Unopened')
        current_location = cellar_data.get('currentLocation', 'At Home')
        sub_location = cellar_data.get('subLocation')
        note_to_self = cellar_data.get('noteToSelf')
        
        # Normalize values
        if volume_number:
            volume_number = round(float(volume_number), 2)
        if volume_unit:
            volume_unit = volume_unit.lower().strip()
        if format_value:
            format_value = format_value.strip().title()
        
        # Check for existing master record
        cursor.execute("""
            SELECT ci."id", ci."collectionID", ci."variantGroupID" 
            FROM "myCellarItems" ci
            JOIN "myCellarCollections" cc ON ci."collectionID" = cc."id"
            WHERE ci."listingID" = %s 
            AND (ci."variant" = %s OR (ci."variant" IS NULL AND %s IS NULL))
            AND ci."quantityVariantID" = 1
            AND UPPER(ci."drinkFormat") = UPPER(%s)
            AND ROUND(CAST(ci."volumeNumber" AS NUMERIC), 2) = %s
            AND LOWER(ci."volumeUnit") = %s
            AND cc."ownerID" = %s
            AND cc."ownerType" = %s
            AND ci."archiveStatus" = FALSE
        """, (
            listing_id, variant, variant, format_value, 
            volume_number, volume_unit, owner_id, owner_type
        ))
        
        master_record = cursor.fetchone()
    
        if not master_record:
            # Create new master record
            cursor.execute("""
                INSERT INTO "myCellarItems" (
                    "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                    "drinkFormat", "volumeNumber", "volumeUnit", "drinkByDate", "drinkOnwardsDate",
                    "currentValueEstimation", "currentValueCurrency", "suggestedFoodPairing",
                    "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                    "purchasePlaceName", "purchaseAddress",
                    "status", "consumption", "currentLocation", "subLocation",
                    "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                ) VALUES (
                    %s, %s, %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING "id"
            """, (
                listing_id, collection_id, variant, 1,
                format_value, volume_number, volume_unit, drink_by_date, drink_onwards_date,
                current_value_estimation, current_value_currency, suggested_food_pairing,
                purchase_date, delivery_date, purchase_price, purchase_currency,
                purchase_place_name, purchase_address,
                status, consumption, current_location, sub_location,
                note_to_self, False, datetime.now(), datetime.now()
            ))
            
            master_id = cursor.fetchone()['id']
            
            # Update variantGroupID to self-reference
            cursor.execute('UPDATE "myCellarItems" SET "variantGroupID" = %s WHERE "id" = %s', (master_id, master_id))
        
            group_variant_id = master_id
            created_bottle_ids = [master_id]
            
            # Create additional bottles if quantity > 1
            if quantity > 1:
                for i in range(1, quantity):
                    cursor.execute("""
                        INSERT INTO "myCellarItems" (
                            "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                            "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                            "purchasePlaceName", "purchaseAddress",
                            "status", "consumption", "currentLocation", "subLocation",
                            "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        ) RETURNING "id"
                    """, (
                        listing_id, collection_id, variant, i + 1, group_variant_id,
                        purchase_date, delivery_date, purchase_price, purchase_currency,
                        purchase_place_name, purchase_address,
                        status, consumption, current_location, sub_location,
                        note_to_self, False, datetime.now(), datetime.now()
                    ))
                    
                    created_bottle_ids.append(cursor.fetchone()['id'])
            
            print(f"Created new master record {master_id} with {quantity} bottle(s)")
        else:
            # Existing master - add bottles to group
            master_id = master_record['id']
            group_variant_id = master_record['variantGroupID']
            existing_collection_id = master_record['collectionID']
            
            # Use existing master's collection
            collection_id = existing_collection_id
            
            # Get next quantityVariantID
            cursor.execute("""
                SELECT MAX("quantityVariantID") as max_id
                FROM "myCellarItems"
                WHERE "variantGroupID" = %s
            """, (group_variant_id,))
            
            result = cursor.fetchone()
            next_variant_id = (result['max_id'] or 1) + 1
            
            created_bottle_ids = []
            
            # Create individual bottles
            for i in range(quantity):
                cursor.execute("""
                    INSERT INTO "myCellarItems" (
                        "listingID", "collectionID", "variant", "quantityVariantID", "variantGroupID",
                        "purchaseDate", "deliveryDate", "purchasePrice", "purchaseCurrency",
                        "purchasePlaceName", "purchaseAddress",
                        "status", "consumption", "currentLocation", "subLocation",
                        "noteToSelf", "archiveStatus", "addedDate", "updatedDate"
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING "id"
                """, (
                    listing_id, collection_id, variant, next_variant_id + i, group_variant_id,
                    purchase_date, delivery_date, purchase_price, purchase_currency,
                    purchase_place_name, purchase_address,
                    status, consumption, current_location, sub_location,
                    note_to_self, False, datetime.now(), datetime.now()
                ))
                
                created_bottle_ids.append(cursor.fetchone()['id'])
            
            print(f"Added {quantity} bottle(s) to existing master {master_id}")
        
        return {
            "masterId": master_id,
            "bottleIds": created_bottle_ids,
            "quantity": quantity
        }

@blueprint.route("/importCellarCsv", methods=['POST'])
def importCellarCsv():
    """Import CSV to cellar with user decisions on duplicates"""
    
    try:
        with db_manager.get_cursor(commit=False) as cursor:
            data = request.get_json()
            owner_type = data.get('ownerType')
            owner_id = data.get('ownerId')
            collection_id = data.get('collectionId')
            import_items = data.get('items', [])

            if not collection_id:
                # Try to find default collection
                cursor.execute("""
                    SELECT "id" FROM "myCellarCollections" 
                    WHERE "ownerID" = %s AND "ownerType" = %s AND "isDefault" = TRUE
                    LIMIT 1
                """, (owner_id, owner_type))
                
                default_collection = cursor.fetchone()

                if default_collection:
                    collection_id = default_collection['id']
                    print(f"Using default collection ID: {collection_id}")
                else:
                    print(f"No collections found, creating default collection")
                    cursor.execute("""
                        INSERT INTO "myCellarCollections" (
                            "ownerID", "ownerType", "collectionName", "isDefault", "isPublic",
                            "createdDate", "updatedDate"
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING "id"
                    """, (
                        owner_id, owner_type, 'My Cellar', True, True,
                        datetime.now(), datetime.now()
                    ))
                    collection_id = cursor.fetchone()['id']
                    cursor.connection.commit()
                    print(f"Created default collection ID: {collection_id}")

            
            # Validate collection belongs to owner
            cursor.execute("""
                SELECT "id" FROM "myCellarCollections" 
                WHERE "id" = %s AND "ownerID" = %s AND "ownerType" = %s
            """, (collection_id, owner_id, owner_type))
            
            if not cursor.fetchone():
                return jsonify({"code": 400, "message": "Invalid collection or collection does not belong to this user"}), 400
        
            imported_count = 0
            created_listings_count = 0
            skipped_count = 0
            errors = []
            
            for item in import_items:
                try:
                    mapped_data = item.get('mappedData', {})
                    selected_match_id = item.get('selectedMatchId')
                    row_number = item.get('rowNumber', 0)
                    
                    # Skip if user chose to skip
                    if selected_match_id == 'skip':
                        skipped_count += 1
                        print(f"Row {row_number} - Skipped by user")
                        continue
                    
                    # Validate required fields
                    if not mapped_data.get('listingName'):
                        errors.append({"rowNumber": row_number, "error": "Missing drink name"})
                        continue
                    
                    # Determine listing ID
                    if selected_match_id == 'create_new':
                        # Create new listing - PASS owner info for tracking
                        listing_id = create_new_listing(cursor, mapped_data, owner_type, owner_id)
                        created_listings_count += 1
                        
                        # Flush the transaction so the listing is visible
                        # for foreign key constraints when adding to cellar
                        conn = cursor.connection
                        conn.commit()
                        
                        # Re-establish cursor after commit
                        cursor = conn.cursor(cursor_factory=RealDictCursor)
                    elif selected_match_id:
                        # Use existing listing
                        try:
                            listing_id = int(selected_match_id)
                        except ValueError:
                            errors.append({"rowNumber": row_number, "error": "Invalid listing ID"})
                            continue
                    else:
                        errors.append({"rowNumber": row_number, "error": "No listing selected"})
                        continue
                    
                    # Prepare cellar data
                    quantity = mapped_data.get('quantity')
                    if quantity is None or quantity < 1:
                        quantity = 1
                    
                    cellar_data = {
                        'listingId': listing_id,
                        'ownerType': owner_type,
                        'ownerId': owner_id,
                        'collectionId': collection_id,
                        'quantity': quantity,
                        'variant': mapped_data.get('variant'),
                        'format': mapped_data.get('drinkFormat', 'Bottle'),
                        'volumeNumber': mapped_data.get('volumeNumber', 750),
                        'volumeUnit': mapped_data.get('volumeUnit', 'ml'),
                        'drinkOnwardsDate': mapped_data.get('drinkOnwardsDate'),
                        'drinkByDate': mapped_data.get('drinkByDate'),
                        'currentValueEstimation': mapped_data.get('currentValueEstimation'),
                        'currentValueCurrency': mapped_data.get('currentValueCurrency', 'USD'),
                        'suggestedFoodPairing': mapped_data.get('suggestedFoodPairing'),
                        'status': mapped_data.get('status', 'In Possession'),
                        'consumption': mapped_data.get('consumption', 'Unopened'),
                        'currentLocation': mapped_data.get('currentLocation', 'At Home'),
                        'subLocation': mapped_data.get('subLocation'),
                        'purchasePrice': mapped_data.get('purchasePrice'),
                        'purchaseCurrency': mapped_data.get('purchaseCurrency', 'USD'),
                        'purchaseDate': mapped_data.get('purchaseDate'),
                        'deliveryDate': mapped_data.get('deliveryDate'),
                        'purchasePlaceName': mapped_data.get('purchasePlaceName'),
                        'purchaseAddress': mapped_data.get('purchaseAddress'),
                        'noteToSelf': mapped_data.get('noteToSelf', '')
                    }
                    
                    # Add to cellar
                    result = add_cellar_item_from_import(cellar_data)
                    imported_count += result['quantity']
                    
                    print(f"Row {row_number} - Successfully imported {result['quantity']} item(s)")
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"Error importing row {item.get('rowNumber', 0)}: {error_msg}")
                    import traceback
                    print(traceback.format_exc())
                    errors.append({
                        "rowNumber": item.get('rowNumber', 0),
                        "error": error_msg
                    })
        
            # Commit all changes
            cursor.connection.commit()
            
            print(f"Import complete - imported: {imported_count}, created: {created_listings_count}, skipped: {skipped_count}, errors: {len(errors)}")
            
            return jsonify({
                "code": 200,
                "message": "Import complete",
                "data": {
                    "importedCount": imported_count,
                    "createdListingsCount": created_listings_count,
                    "skippedCount": skipped_count,
                    "errorCount": len(errors),
                    "errors": errors
                }
            }), 200
        
    except Exception as e:
        print(f"Import failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "code": 500,
            "message": f"Import failed: {str(e)}"
        }), 500