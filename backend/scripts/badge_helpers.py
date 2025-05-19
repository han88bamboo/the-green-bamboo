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
                    VALUES (%s, %s, 1, 1)
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
            VALUES (%s, %s, 1, 1)
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
                VALUES (%s, %s, 1, 1)
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