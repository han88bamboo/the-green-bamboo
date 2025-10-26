// templates/MinimalTemplate.js
import Konva from "konva";

const renderTags = (layer, tags, yPos, WIDTH) => {
  const tagSpacing = 20;
  const tagHeight = 50;
  const tagFontSize = 24;
  const tagFontFamily = "Arial";
  const tagFill = "#333333"; // Dark text
  const tagBgFill = "#EEEEEE"; // Light grey background

  const tagObjects = tags.map(tag => {
    const width = tag.length * 16 + 40;
    return { text: tag, width: width };
  });

  const totalWidth = tagObjects.reduce((sum, tag) => sum + tag.width, 0) + Math.max(0, tagObjects.length - 1) * tagSpacing;

  let currentX = (WIDTH - totalWidth) / 2;

  tagObjects.forEach(({ text, width }) => {
    const tagBg = new Konva.Rect({
      x: currentX,
      y: yPos,
      width: width,
      height: tagHeight,
      fill: tagBgFill,
      cornerRadius: 25,
    });
    layer.add(tagBg);

    const tagText = new Konva.Text({
      text: text,
      x: currentX + 20,
      y: yPos + (tagHeight - tagFontSize) / 2,
      fontSize: tagFontSize,
      fontFamily: tagFontFamily,
      fill: tagFill,
    });
    layer.add(tagText);

    currentX += width + tagSpacing;
  });

  return yPos + tagHeight;
};


export const createMinimalTemplate = async (layer, data, images) => {
  const WIDTH = 1080;
  const HEIGHT = 1920;

  // 1. Background - REMOVED for transparency

  // 2. Beverage Image (if available)
  if (images.beverage) {
    const beverageImg = new Konva.Image({
      image: images.beverage,
      x: WIDTH / 2,
      y: 400,
      offsetX: 200,
      offsetY: 200,
      width: 400,
      height: 400,
      cornerRadius: 20,
      // Adding a light border in case the image is transparent too
      stroke: '#EEEEEE',
      strokeWidth: 2,
    });
    layer.add(beverageImg);
  }

  // 3. Beverage Name
  const nameText = new Konva.Text({
    text: data.beverage.name,
    x: 80,
    y: 750,
    width: WIDTH - 160,
    fontSize: 80,
    fontFamily: "Arial",
    fontStyle: "bold",
    fill: "#333333", // Dark text
    align: "center",
  });
  layer.add(nameText);

  // 4. Type/ABV
  const subtitleText = new Konva.Text({
    text: `${data.beverage.type} • ${data.beverage.abv}%`,
    x: 80,
    y: nameText.y() + nameText.height() + 20,
    width: WIDTH - 160,
    fontSize: 36,
    fontFamily: "Arial",
    fill: "#555555", // Slightly lighter dark text
    opacity: 0.8,
    align: "center",
  });
  layer.add(subtitleText);

  // 5. Rating (Large)
  const ratingGroup = new Konva.Group({
    x: WIDTH / 2,
    y: subtitleText.y() + subtitleText.height() + 150,
  });

  const ratingBg = new Konva.Circle({
    x: 0,
    y: 0,
    radius: 120,
    fill: "#EEEEEE", // Light grey background
  });
  ratingGroup.add(ratingBg);

  const ratingText = new Konva.Text({
    text: data.review.rating.toFixed(1),
    x: -120,
    y: -50,
    fontSize: 96,
    fontFamily: "Arial",
    fontStyle: "bold",
    fill: "#333333", // Dark text
    width: 240,
    align: "center",
  });
  ratingGroup.add(ratingText);

  const starsText = new Konva.Text({
    text: "★★★★★".slice(0, Math.round(data.review.rating)) + "☆☆☆☆☆".slice(Math.round(data.review.rating)),
    x: -120,
    y: 50,
    fontSize: 40,
    fill: "#FFC107", // Brighter gold
    width: 240,
    align: "center",
  });
  ratingGroup.add(starsText);

  layer.add(ratingGroup);

  let currentY = ratingGroup.y() + 120 + 50;

  // 6. Location (conditional)
  if (data.review.location) {
    const locationText = new Konva.Text({
      text: `📍 ${data.review.location}`,
      x: 80,
      y: currentY,
      width: WIDTH - 160,
      fontSize: 32,
      fontFamily: "Arial",
      fill: "#555555", // Lighter dark text
      align: "center",
    });
    layer.add(locationText);
    currentY += locationText.height() + 40;
  }

  // 7. Flavour Tags (Top 3)
  if (data.review.flavourTags && data.review.flavourTags.length > 0) {
    const flavourTags = data.review.flavourTags.slice(0, 3);
    currentY = renderTags(layer, flavourTags, currentY, WIDTH) + 20;
  }

  // 8. Action Tags (Top 3)
  if (data.review.observationTags && data.review.observationTags.length > 0) {
    const actionTags = data.review.observationTags.slice(0, 3);
    currentY = renderTags(layer, actionTags, currentY, WIDTH) + 40;
  }

  // 9. Date (conditional)
  const reviewDate = new Date(data.review.date);
  if (!isNaN(reviewDate)) {
    const dateText = new Konva.Text({
      text: reviewDate.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      }),
      x: 80,
      y: currentY,
      width: WIDTH - 160,
      fontSize: 28,
      fontFamily: "Arial",
      fill: "#777777", // Lighter dark text
      opacity: 0.8,
      align: "center",
    });
    layer.add(dateText);
  }

  // 10. Footer: Username and App Logo
  const usernameText = new Konva.Text({
    text: data.user.name,
    x: 80,
    y: HEIGHT - 100,
    fontSize: 32,
    fontFamily: "Arial",
    fill: "#555555", // Lighter dark text
    opacity: 0.8,
  });
  layer.add(usernameText);

  const logoText = new Konva.Text({
    text: "Drink-x",
    x: WIDTH - 280, // Bounding box start
    y: HEIGHT - 100,
    width: 200, // Bounding box width
    fontSize: 36,
    fontFamily: "Arial",
    fontStyle: "bold",
    fill: "#555555", // Lighter dark text
    opacity: 0.7,
    align: "right",
  });
  layer.add(logoText);
};
