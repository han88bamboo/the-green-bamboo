// templates/MinimalTemplate.js
import Konva from "konva";

export const createMinimalTemplate = async (layers, data) => {
  const { bg, fg } = layers;
  const width = 1080;
  const height = 1350;

  // Safe rating formatting
  const rating = Number(data.review?.rating) || 0;
  const ratingText = rating.toFixed(1);

  // Background - for preview but not for download
  const bgRect = new Konva.Rect({
    x: 0,
    y: 0,
    width: width,
    height: height * 2,
    fill: "#b0b0b0", // Single solid color instead
  });
  bg.add(bgRect);

  // Checkerboard pattern overlay - to simulate transparency, but not for download
  const patternSize = 60;
  const cols = Math.ceil(width / patternSize);
  const rows = Math.ceil((height * 2) / patternSize);

  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      if ((i + j) % 2 === 0) {
        const square = new Konva.Rect({
          x: i * patternSize,
          y: j * patternSize,
          width: patternSize,
          height: patternSize,
          fill: "#4f4e4eff", // Lighter gray instead of white
          opacity: 0.6, // More visible
        });
        bg.add(square);
      }
    }
  }

  // Rating Section (Top Center)
  const ratingGroup = new Konva.Group({
    x: width / 2,
    y: 150,
  });

  // Rating Number
  const ratingNum = new Konva.Text({
    x: -150,
    y: 200,
    text: ratingText,
    fontSize: 120,
    fontFamily: "Arial, sans-serif",
    fontStyle: "bold",
    fill: "#ffffff",
    stroke: "#333333",
    strokeWidth: 2,
  });
  ratingGroup.add(ratingNum);

  // Star
  const star = new Konva.Star({
    x: 110,
    y: 260,
    numPoints: 5,
    innerRadius: 30,
    outerRadius: 60,
    fill: "#FFA500",
    stroke: "#FF8C00",
    strokeWidth: 3,
  });
  ratingGroup.add(star);

  fg.add(ratingGroup);

  // Review Comment (Center)
  if (data.review?.reviewDesc) {
    const comment = new Konva.Text({
      x: 100,
      y: 500,
      text: `"${data.review.reviewDesc}"`,
      fontSize: 52,
      fontFamily: "Arial, sans-serif",
      fontStyle: "bold",
      fill: "#ffffff",
      stroke: "#ffffffff",
      strokeWidth: 1.5,
      width: width - 200,
      height: 150,
      ellipsis: true, // ✅ This adds "..." when text overflows
      align: "center",
      wrap: "word",
      lineHeight: 1.3,
    });
    fg.add(comment);
  }

  // Tags Section (flavor profiles and characteristics)
  const tags = [];

  // Get flavor tags from review data
  if (data.review?.flavorTags && Array.isArray(data.review.flavorTags)) {
    tags.push(...data.review.flavorTags.slice(0, 3));
  }

  // Get characteristic tags
  if (
    data.review?.characteristics &&
    Array.isArray(data.review.characteristics)
  ) {
    tags.push(...data.review.characteristics.slice(0, 3));
  }

  // Default tags if none provided
  if (tags.length === 0) {
    tags.push("Smooth", "Balanced", "Flavorful");
  }

  // Tag colors
  // const tagColors = [
  //   { bg: "#E8D5A8", text: "#5C4B2E" }, // Cream/tan
  //   { bg: "#7B9FE8", text: "#1E3A5F" }, // Blue
  //   { bg: "#C77EB5", text: "#4A1E40" }, // Purple/pink
  //   { bg: "#F39C6B", text: "#5C2E1E" }, // Orange
  //   { bg: "#FFB84D", text: "#5C3E1E" }, // Yellow/gold
  // ];

  // Draw tags in rows
  const tagStartY = 680;
  const tagSpacing = 20;
  const maxTagsPerRow = 3;
  let currentX = width / 2;
  let currentY = tagStartY;
  let currentRowTags = 0;

  tags.forEach((tag, index) => {
    // const colorScheme = tagColors[index % tagColors.length];

    // Calculate tag dimensions
    const tempText = new Konva.Text({
      text: tag,
      fontSize: 36,
      fontFamily: "Arial, sans-serif",
      fontStyle: "bold",
    });
    const tagWidth = tempText.width() + 60;
    const tagHeight = 60;

    // Move to next row if needed
    if (currentRowTags >= maxTagsPerRow) {
      currentY += tagHeight + tagSpacing;
      currentRowTags = 0;
    }

    // Calculate position for centering
    if (currentRowTags === 0) {
      const rowTags = Math.min(maxTagsPerRow, tags.length - index);
      const rowWidth = rowTags * (tagWidth + tagSpacing) - tagSpacing;
      currentX = (width - rowWidth) / 2;
    }

    // Tag background
    const tagBg = new Konva.Rect({
      x: currentX,
      y: currentY,
      width: tagWidth,
      height: tagHeight,
      fill: tag.color,
      cornerRadius: 30,
      shadowColor: "rgba(0, 0, 0, 0.3)",
      shadowBlur: 10,
      shadowOffset: { x: 0, y: 4 },
    });
    fg.add(tagBg);

    // Tag text
    const tagText = new Konva.Text({
      x: currentX,
      y: currentY + 12,
      text: tag.name,
      fontSize: 36,
      fontFamily: "Arial, sans-serif",
      fontStyle: "bold",
      fill: "#ffffff",
      width: tagWidth,
      align: "center",
    });
    fg.add(tagText);

    currentX += tagWidth + tagSpacing;
    currentRowTags++;
  });

  // Beverage Name (Bottom)
  // const beverageName = new Konva.Text({
  //   x: 80,
  //   y: 220,
  //   text: data.beverage?.name || "Unknown Beverage",
  //   fontSize: 100,
  //   fontFamily: "Arial, sans-serif",
  //   fontStyle: "bold",
  //   fill: "#ffffff",
  //   stroke: "#333333",
  //   strokeWidth: 2,
  //   width: width - 160,
  //   align: "center",
  // });
  // fg.add(beverageName);

  // User Info
  const userName = new Konva.Text({
    x: 80,
    y: 960,
    text: `— ${data.user?.name || "Anonymous"}`,
    fontSize: 32,
    fontFamily: "Arial, sans-serif",
    fill: "#ffffff",
    opacity: 0.9,
    width: width - 160,
    align: "center",
  });
  fg.add(userName);

  fg.batchDraw();
}