def process_badges(conn, cur, user_id, badge_triggers):
    badges_awarded = []
    
    for trigger in badge_triggers:
        action_type = trigger['actionType']
        mapping_type = trigger['mappingType']
        primary_value = trigger['primaryValue']
        secondary_value = trigger['secondaryValue']
        
        # 1. Find badges matching this trigger
        if mapping_type == 'Action':
            # For action badges, we check relatedEntity
            cur.execute("""
                SELECT b.* FROM "badges" b
                WHERE b."badgeType" = 'Action' AND b."relatedEntity" = %s
            """, (primary_value,))
        else:
            # For other badges, we check the mappings table
            if secondary_value:
                # Category badge (with secondary value)
                cur.execute("""
                    SELECT b.* FROM "badges" b
                    JOIN "badgeMappings" bm ON b.id = bm."badgeId"
                    WHERE bm."mappingType" = %s AND bm."primaryValue" = %s AND bm."secondaryValue" = %s
                """, (mapping_type, primary_value, secondary_value))
            else:
                # Country or DrinkType badge (no secondary value)
                cur.execute("""
                    SELECT b.* FROM "badges" b
                    JOIN "badgeMappings" bm ON b.id = bm."badgeId"
                    WHERE bm."mappingType" = %s AND bm."primaryValue" = %s AND bm."secondaryValue" IS NULL
                """, (mapping_type, primary_value))
        
        badges = cur.fetchall()
        
        # 2. For each matching badge, update user's progress
        for badge in badges:
            badge_id = badge['id']
            
            # Check if user already has this badge
            cur.execute("""
                SELECT * FROM "userBadges" 
                WHERE "userId" = %s AND "badgeId" = %s
            """, (user_id, badge_id))
            
            user_badge = cur.fetchone()
            
            if user_badge:
                # User already has this badge, update progress
                current_level = user_badge['currentLevel']
                current_progress = user_badge['currentProgress'] + 1
                
                # Get rule for this level
                cur.execute("""
                    SELECT * FROM "badgeRules"
                    WHERE "actionType" = %s
                    AND %s BETWEEN "levelStart" AND "levelEnd"
                """, (action_type, current_level))
                
                rule = cur.fetchone()
                
                if rule:
                    actions_required = rule['actionsRequired']
                    
                    # Check if user has enough actions to level up
                    if current_progress >= actions_required:
                        # Level up!
                        cur.execute("""
                            UPDATE "userBadges"
                            SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                            WHERE "userId" = %s AND "badgeId" = %s
                            RETURNING "currentLevel"
                        """, (current_level + 1, user_id, badge_id))
                        
                        new_level = cur.fetchone()['currentLevel']
                        
                        badges_awarded.append({
                            "badgeId": badge_id, 
                            "badgeName": badge['badgeName'],
                            "badgeDesc": badge['badgeDesc'],
                            "badgePhoto": badge['badgePhoto'],
                            "newLevel": new_level,
                            "isNewBadge": False
                        })
                        
                    else:
                        # Just update progress
                        cur.execute("""
                            UPDATE "userBadges"
                            SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                            WHERE "userId" = %s AND "badgeId" = %s
                        """, (current_progress, user_id, badge_id))
            else:
                # User doesn't have this badge yet, create it
                cur.execute("""
                    INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                    VALUES (%s, %s, 1, 0)
                    RETURNING "currentLevel"
                """, (user_id, badge_id))
                
                badges_awarded.append({
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'], 
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": 1,
                    "isNewBadge": True
                })
    
    # Commit all badge updates
    conn.commit()
    
    return badges_awarded

def update_badge_progress(conn, cur, user_id, related_entity, badge_type, change_amount):
    # Find the badge
    if badge_type == 'Action':
        cur.execute("""
            SELECT b.* FROM "badges" b
            WHERE b."badgeType" = 'Action' AND b."relatedEntity" = %s
        """, (related_entity,))
    else:
        # For other badge types using mappings table - can be expanded if needed
        return None
    
    badge = cur.fetchone()
    
    if not badge:
        return None
        
    badge_id = badge['id']
    
    # Check if user has this badge
    cur.execute("""
        SELECT * FROM "userBadges" 
        WHERE "userId" = %s AND "badgeId" = %s
    """, (user_id, badge_id))
    
    user_badge = cur.fetchone()
    
    if not user_badge and change_amount < 0:
        # User doesn't have this badge and we're trying to decrease - nothing to do
        return None
    
    if not user_badge and change_amount > 0:
        # User doesn't have this badge yet and we're adding - create it
        cur.execute("""
            INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
            VALUES (%s, %s, 1, 0)
            RETURNING "currentLevel"
        """, (user_id, badge_id))
        
        conn.commit()
        
        return {
            "badgeId": badge_id,
            "badgeName": badge['badgeName'],
            "badgeDesc": badge['badgeDesc'], 
            "badgePhoto": badge['badgePhoto'],
            "newLevel": 1,
            "isNewBadge": True,
            "changeAmount": change_amount
        }
    
    # User has the badge - update progress
    current_level = user_badge['currentLevel']
    current_progress = user_badge['currentProgress']
    
    # Get rule for this level to determine actions required for next level
    cur.execute("""
        SELECT * FROM "badgeRules"
        WHERE "actionType" = %s
        AND %s BETWEEN "levelStart" AND "levelEnd"
    """, (related_entity, current_level))
    
    rule = cur.fetchone()
    
    if not rule:
        # No rule found - don't update
        return None
    
    actions_required = rule['actionsRequired']
    
    if change_amount > 0:
        # Increasing progress
        new_progress = current_progress + change_amount
        
        # Check if user levels up
        if new_progress >= actions_required:
            # Level up!
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level + 1, user_id, badge_id))
            
            conn.commit()
            new_level = cur.fetchone()['currentLevel']
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": new_level,
                "previousLevel": current_level,
                "isNewBadge": False,
                "changeAmount": change_amount
            }
        else:
            # Just update progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False,
                "changeAmount": change_amount
            }
    else:
        # Decreasing progress
        new_progress = max(0, current_progress + change_amount)
        
        # OPTION 2: If progress drops to 0, completely remove the badge
        if new_progress == 0:
            cur.execute("""
                DELETE FROM "userBadges"
                WHERE "userId" = %s AND "badgeId" = %s
            """, (user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "removed": True,
                "changeAmount": change_amount
            }
        else:
            # Just reduce progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False,
                "changeAmount": change_amount
            }
        
def process_new_drink_badge(conn, cur, user_id):
    try:
        # Find the "Brew-tiful Mind" badge
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'NewDrink'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'NewDrink' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        if not user_badge:
            # User doesn't have this badge yet - create it
            cur.execute("""
                INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                VALUES (%s, %s, 1, 0)
                RETURNING "currentLevel"
            """, (user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'], 
                "badgePhoto": badge['badgePhoto'],
                "newLevel": 1,
                "isNewBadge": True
            }
            
        # User already has this badge - update progress
        current_level = user_badge['currentLevel']
        current_progress = user_badge['currentProgress']
        
        # Get rule for this level
        cur.execute("""
            SELECT * FROM "badgeRules"
            WHERE "actionType" = 'NewDrink'
            AND %s BETWEEN "levelStart" AND "levelEnd"
        """, (current_level,))
        
        rule = cur.fetchone()
        if not rule:
            print(f"No badge rule found for level {current_level}")
            return None
            
        actions_required = rule['actionsRequired']
        new_progress = current_progress + 1
        
        # Check if user has enough actions to level up
        if new_progress >= actions_required:
            # Level up!
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level + 1, user_id, badge_id))
            
            conn.commit()
            new_level = cur.fetchone()['currentLevel']
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": new_level,
                "previousLevel": current_level,
                "isNewBadge": False
            }
        else:
            # Just update progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False
            }
    except Exception as e:
        print(f"Error processing NewDrink badge: {str(e)}")
        return None
    
def process_club_post_badge(conn, cur, user_id):
    """
    Award or update the ClubPost badge for a user when they add a club post
    
    Args:
        conn: Database connection
        cur: Database cursor
        user_id: ID of the user who added the post
        
    Returns:
        Dictionary with badge update information or None if no update
    """
    try:
        # Find the "In Da Club We All Fam" badge
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'ClubPost'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'ClubPost' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        if not user_badge:
            # User doesn't have this badge yet - create it
            cur.execute("""
                INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                VALUES (%s, %s, 1, 0)
                RETURNING "currentLevel"
            """, (user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'], 
                "badgePhoto": badge['badgePhoto'],
                "newLevel": 1,
                "isNewBadge": True
            }
            
        # User already has this badge - update progress
        current_level = user_badge['currentLevel']
        current_progress = user_badge['currentProgress']
        
        # Get rule for this level
        cur.execute("""
            SELECT * FROM "badgeRules"
            WHERE "actionType" = 'ClubPost'
            AND %s BETWEEN "levelStart" AND "levelEnd"
        """, (current_level,))
        
        rule = cur.fetchone()
        if not rule:
            print(f"No badge rule found for level {current_level}")
            return None
            
        actions_required = rule['actionsRequired']
        new_progress = current_progress + 1
        
        # Check if user has enough actions to level up
        if new_progress >= actions_required:
            # Level up!
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level + 1, user_id, badge_id))
            
            conn.commit()
            new_level = cur.fetchone()['currentLevel']
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": new_level,
                "previousLevel": current_level,
                "isNewBadge": False
            }
        else:
            # Just update progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False
            }
    except Exception as e:
        print(f"Error processing ClubPost badge: {str(e)}")
        return None
    
def process_comment_badge(conn, cur, user_id):
    try:
        # Find the "Rising Contributor" badge
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'Comment'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'Comment' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        if not user_badge:
            # User doesn't have this badge yet - create it
            cur.execute("""
                INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                VALUES (%s, %s, 1, 0)
                RETURNING "currentLevel"
            """, (user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'], 
                "badgePhoto": badge['badgePhoto'],
                "newLevel": 1,
                "isNewBadge": True
            }
            
        # User already has this badge - update progress
        current_level = user_badge['currentLevel']
        current_progress = user_badge['currentProgress']
        
        # Get rule for this level
        cur.execute("""
            SELECT * FROM "badgeRules"
            WHERE "actionType" = 'Comment'
            AND %s BETWEEN "levelStart" AND "levelEnd"
        """, (current_level,))
        
        rule = cur.fetchone()
        if not rule:
            print(f"No badge rule found for level {current_level}")
            return None
            
        actions_required = rule['actionsRequired']
        new_progress = current_progress + 1
        
        # Check if user has enough actions to level up
        if new_progress >= actions_required:
            # Level up!
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level + 1, user_id, badge_id))
            
            conn.commit()
            new_level = cur.fetchone()['currentLevel']
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": new_level,
                "previousLevel": current_level,
                "isNewBadge": False
            }
        else:
            # Just update progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False
            }
    except Exception as e:
        print(f"Error processing Comment badge: {str(e)}")
        return None
    
def process_question_badge(conn, cur, user_id):
    try:
        # Find the "Shoot Your Shot" badge
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'Question'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'Question' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        if not user_badge:
            # User doesn't have this badge yet - create it
            cur.execute("""
                INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                VALUES (%s, %s, 1, 0)
                RETURNING "currentLevel"
            """, (user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'], 
                "badgePhoto": badge['badgePhoto'],
                "newLevel": 1,
                "isNewBadge": True
            }
            
        # User already has this badge - update progress
        current_level = user_badge['currentLevel']
        current_progress = user_badge['currentProgress']
        
        # Get rule for this level
        cur.execute("""
            SELECT * FROM "badgeRules"
            WHERE "actionType" = 'Question'
            AND %s BETWEEN "levelStart" AND "levelEnd"
        """, (current_level,))
        
        rule = cur.fetchone()
        if not rule:
            print(f"No badge rule found for level {current_level}")
            return None
            
        actions_required = rule['actionsRequired']
        new_progress = current_progress + 1
        
        # Check if user has enough actions to level up
        if new_progress >= actions_required:
            # Level up!
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level + 1, user_id, badge_id))
            
            conn.commit()
            new_level = cur.fetchone()['currentLevel']
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": new_level,
                "previousLevel": current_level,
                "isNewBadge": False
            }
        else:
            # Just update progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False
            }
    except Exception as e:
        print(f"Error processing Question badge: {str(e)}")
        return None
    
def process_upvote_badge(conn, cur, user_id, is_new_upvote=False, is_removed_upvote=False):
    try:
        # Find the "DrinkGPT" badge
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'Upvote'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'Upvote' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        # Handle a new upvote (increasing badge progress)
        if is_new_upvote:
            if not user_badge:
                # User doesn't have this badge yet - create it
                cur.execute("""
                    INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                    VALUES (%s, %s, 1, 0)
                    RETURNING "currentLevel"
                """, (user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'], 
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": 1,
                    "isNewBadge": True
                }
                
            # User already has this badge - update progress
            current_level = user_badge['currentLevel']
            current_progress = user_badge['currentProgress'] + 1
            
            # Get rule for this level
            cur.execute("""
                SELECT * FROM "badgeRules"
                WHERE "actionType" = 'Upvote'
                AND %s BETWEEN "levelStart" AND "levelEnd"
            """, (current_level,))
            
            rule = cur.fetchone()
            if not rule:
                print(f"No badge rule found for level {current_level}")
                return None
                
            actions_required = rule['actionsRequired']
            
            # Check if user has enough actions to level up
            if current_progress >= actions_required and current_level < 100:
                # Level up!
                cur.execute("""
                    UPDATE "userBadges"
                    SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                    WHERE "userId" = %s AND "badgeId" = %s
                    RETURNING "currentLevel"
                """, (current_level + 1, user_id, badge_id))
                
                conn.commit()
                new_level = cur.fetchone()['currentLevel']
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": new_level,
                    "previousLevel": current_level,
                    "isNewBadge": False,
                    "change": "increase"
                }
            else:
                # Just update progress
                cur.execute("""
                    UPDATE "userBadges"
                    SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                    WHERE "userId" = %s AND "badgeId" = %s
                """, (current_progress, user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": current_level,
                    "newProgress": current_progress,
                    "isNewBadge": False,
                    "change": "increase"
                }
        
        # Handle removing an upvote (decreasing badge progress)
        elif is_removed_upvote and user_badge:
            current_level = user_badge['currentLevel']
            current_progress = user_badge['currentProgress'] - 1
            
            # Get rules for level calculations
            cur.execute("""
                SELECT * FROM "badgeRules"
                WHERE "actionType" = 'Upvote'
                ORDER BY "levelStart"
            """)
            
            rules = cur.fetchall()
            
            # Helper function to get actions needed for a level
            def actions_needed_for_level(level):
                for rule in rules:
                    if rule['levelStart'] <= level <= rule['levelEnd']:
                        return rule['actionsRequired']
                return rules[-1]['actionsRequired'] if rules else 1
            
            # If progress goes negative, we need to demote the level
            while current_progress < 0 and current_level > 1:
                current_level -= 1
                current_progress += actions_needed_for_level(current_level)
            
            # If at level 1 with negative progress, remove the badge
            if current_level == 1 and current_progress < 0:
                cur.execute("""
                    DELETE FROM "userBadges"
                    WHERE "userId" = %s AND "badgeId" = %s
                """, (user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "removed": True,
                    "change": "decrease"
                }
            else:
                # Update the badge with new level and progress
                cur.execute("""
                    UPDATE "userBadges"
                    SET "currentLevel" = %s, "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                    WHERE "userId" = %s AND "badgeId" = %s
                """, (current_level, current_progress, user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": current_level,
                    "newProgress": current_progress,
                    "isLevelDown": current_level < user_badge['currentLevel'],
                    "change": "decrease"
                }
                
        return None
        
    except Exception as e:
        print(f"Error processing Upvote badge: {str(e)}")
        return None
    
def process_public_list_badge(conn, cur, user_id, list_change):
    try:
        # Find the "List-o-mania" badge
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'PublicList'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'PublicList' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        # Handle positive list change (creating lists)
        if list_change > 0:
            if not user_badge:
                # User doesn't have this badge yet - create it
                # Set progress to the number of lists created
                #                 
                cur.execute("""
                    INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                    VALUES (%s, %s, 1, 0)
                    RETURNING "currentLevel"
                """, (user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'], 
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": 1,
                    "isNewBadge": True
                }
                
            # User already has this badge - update progress
            current_level = user_badge['currentLevel']
            current_progress = user_badge['currentProgress'] + list_change
            
            # Get rule for this level
            cur.execute("""
                SELECT * FROM "badgeRules"
                WHERE "actionType" = 'PublicList'
                AND %s BETWEEN "levelStart" AND "levelEnd"
            """, (current_level,))
            
            rule = cur.fetchone()
            if not rule:
                print(f"No badge rule found for level {current_level}")
                return None
                
            actions_required = rule['actionsRequired']
            
            # Process multiple level ups if many lists were created at once
            levels_gained = 0
            while current_progress >= actions_required and current_level < 100:
                current_progress -= actions_required
                current_level += 1
                levels_gained += 1
                
                # Get new rule for the next level
                cur.execute("""
                    SELECT * FROM "badgeRules"
                    WHERE "actionType" = 'PublicList'
                    AND %s BETWEEN "levelStart" AND "levelEnd"
                """, (current_level,))
                
                new_rule = cur.fetchone()
                if new_rule:
                    actions_required = new_rule['actionsRequired']
                else:
                    break
            
            # Update the badge
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level, current_progress, user_id, badge_id))
            
            conn.commit()
            
            if levels_gained > 0:
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": current_level,
                    "previousLevel": user_badge['currentLevel'],
                    "levelsGained": levels_gained,
                    "isNewBadge": False,
                    "change": "increase"
                }
            else:
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": current_level,
                    "newProgress": current_progress,
                    "isNewBadge": False,
                    "change": "increase"
                }
        
        # Handle negative list change (deleting lists)
        elif list_change < 0 and user_badge:
            current_level = user_badge['currentLevel']
            current_progress = user_badge['currentProgress'] + list_change  # list_change is negative
            
            # Get rules for level calculations
            cur.execute("""
                SELECT * FROM "badgeRules"
                WHERE "actionType" = 'PublicList'
                ORDER BY "levelStart"
            """)
            
            rules = cur.fetchall()
            
            # Helper function to get actions needed for a level
            def actions_needed_for_level(level):
                for rule in rules:
                    if rule['levelStart'] <= level <= rule['levelEnd']:
                        return rule['actionsRequired']
                return rules[-1]['actionsRequired'] if rules else 1
            
            # If progress goes negative, we need to demote the level
            while current_progress < 0 and current_level > 1:
                current_level -= 1
                current_progress += actions_needed_for_level(current_level)
            
            # If at level 1 with negative progress, remove the badge
            if current_level == 1 and current_progress < 0:
                cur.execute("""
                    DELETE FROM "userBadges"
                    WHERE "userId" = %s AND "badgeId" = %s
                """, (user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "removed": True,
                    "change": "decrease"
                }
            else:
                # Update the badge with new level and progress
                cur.execute("""
                    UPDATE "userBadges"
                    SET "currentLevel" = %s, "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                    WHERE "userId" = %s AND "badgeId" = %s
                """, (current_level, current_progress, user_id, badge_id))
                
                conn.commit()
                
                return {
                    "badgeId": badge_id,
                    "badgeName": badge['badgeName'],
                    "badgeDesc": badge['badgeDesc'],
                    "badgePhoto": badge['badgePhoto'],
                    "newLevel": current_level,
                    "newProgress": current_progress,
                    "isLevelDown": current_level < user_badge['currentLevel'],
                    "change": "decrease"
                }
                
        return None
        
    except Exception as e:
        print(f"Error processing PublicList badge: {str(e)}")
        return None
    
def process_event_attendance_badge(conn, cur, user_id):
    try:
        cur.execute("""
            SELECT * FROM "badges" 
            WHERE "badgeType" = 'Action' AND "relatedEntity" = 'EventAttendance'
        """)
        
        badge = cur.fetchone()
        if not badge:
            print("No 'EventAttendance' badge found in the database")
            return None
            
        badge_id = badge['id']
        
        # Check if user already has this badge
        cur.execute("""
            SELECT * FROM "userBadges" 
            WHERE "userId" = %s AND "badgeId" = %s
        """, (user_id, badge_id))
        
        user_badge = cur.fetchone()
        
        if not user_badge:
            # User doesn't have this badge yet - create it
            cur.execute("""
                INSERT INTO "userBadges" ("userId", "badgeId", "currentLevel", "currentProgress")
                VALUES (%s, %s, 1, 0)
                RETURNING "currentLevel"
            """, (user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'], 
                "badgePhoto": badge['badgePhoto'],
                "newLevel": 1,
                "isNewBadge": True
            }
            
        # User already has this badge - update progress
        current_level = user_badge['currentLevel']
        current_progress = user_badge['currentProgress']
        
        # Get rule for this level
        cur.execute("""
            SELECT * FROM "badgeRules"
            WHERE "actionType" = 'EventAttendance'
            AND %s BETWEEN "levelStart" AND "levelEnd"
        """, (current_level,))
        
        rule = cur.fetchone()
        if not rule:
            print(f"No badge rule found for level {current_level}")
            return None
            
        actions_required = rule['actionsRequired']
        new_progress = current_progress + 1
        
        # Check if user has enough actions to level up
        if new_progress >= actions_required:
            # Level up!
            cur.execute("""
                UPDATE "userBadges"
                SET "currentLevel" = %s, "currentProgress" = 0, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
                RETURNING "currentLevel"
            """, (current_level + 1, user_id, badge_id))
            
            conn.commit()
            new_level = cur.fetchone()['currentLevel']
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": new_level,
                "previousLevel": current_level,
                "isNewBadge": False
            }
        else:
            # Just update progress
            cur.execute("""
                UPDATE "userBadges"
                SET "currentProgress" = %s, "lastUpdated" = CURRENT_TIMESTAMP
                WHERE "userId" = %s AND "badgeId" = %s
            """, (new_progress, user_id, badge_id))
            
            conn.commit()
            
            return {
                "badgeId": badge_id,
                "badgeName": badge['badgeName'],
                "badgeDesc": badge['badgeDesc'],
                "badgePhoto": badge['badgePhoto'],
                "newLevel": current_level,
                "newProgress": new_progress,
                "isNewBadge": False
            }
    except Exception as e:
        print(f"Error processing EventAttendance badge: {str(e)}")
        return None