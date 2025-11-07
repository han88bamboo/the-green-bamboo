// Utility functions for parsing action tags with embedded colors

/**
 * Parse an action tag to extract display text and color
 * @param {string} tag - Tag in format "Display Text#hexcode" or just "Display Text"
 * @returns {Object} - { text: string, color: string }
 */
export const parseActionTag = (tag) => {
  if (!tag || typeof tag !== 'string') {
    return { text: '', color: '#f0b358' };
  }
  
  const hashIndex = tag.lastIndexOf('#');
  if (hashIndex === -1 || hashIndex === tag.length - 1) {
    // No hash or hash at end - treat as text-only tag
    return { text: tag, color: '#f0b358' };
  }
  
  const text = tag.substring(0, hashIndex);
  const colorPart = tag.substring(hashIndex + 1);
  
  // Validate hex color (must be exactly 6 characters, valid hex)
  const isValidHex = /^[0-9A-Fa-f]{6}$/.test(colorPart);
  const color = isValidHex ? '#' + colorPart : '#f0b358';
  
  return { text, color };
};

/**
 * Get just the display text from a tag
 * @param {string} tag - Tag in any format
 * @returns {string} - Display text only
 */
export const getTagDisplayText = (tag) => {
  return parseActionTag(tag).text;
};

/**
 * Get the color for a tag
 * @param {string} tag - Tag in any format
 * @returns {string} - Hex color code
 */
export const getTagColor = (tag) => {
  return parseActionTag(tag).color;
};