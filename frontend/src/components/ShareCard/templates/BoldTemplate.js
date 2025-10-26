// templates/BoldTemplate.js
import Konva from "konva";
//import { addGradientBackground } from "@/utils/konvaHelpers";

export const createBoldTemplate = async (layer, data, images) => {
  const WIDTH = 1080;
  const HEIGHT = 1920;

  // Black background
  const bg = new Konva.Rect({
    x: 0,
    y: 0,
    width: WIDTH,
    height: HEIGHT,
    fill: "#000000",
  });
  layer.add(bg);

  // Large beverage image taking up top half
  if (images.beverage) {
    const beverageImg = new Konva.Image({
      image: images.beverage,
      x: 0,
      y: 0,
      width: WIDTH,
      height: 960,
      crop: {
        x: 0,
        y: 0,
        width: images.beverage.width,
        height: images.beverage.height,
      },
    });
    layer.add(beverageImg);

    // Gradient overlay on image
    const overlay = new Konva.Rect({
      x: 0,
      y: 0,
      width: WIDTH,
      height: 960,
      fillLinearGradientStartPoint: { x: 0, y: 500 },
      fillLinearGradientEndPoint: { x: 0, y: 960 },
      fillLinearGradientColorStops: [0, "rgba(0,0,0,0)", 1, "rgba(0,0,0,0.8)"],
    });
    layer.add(overlay);
  }

  // Bold rating with accent color
  const ratingText = new Konva.Text({
    text: data.review.rating.toFixed(1),
    x: 60,
    y: 1000,
    fontSize: 120,
    fontFamily: "Arial",
    fontStyle: "bold",
    fill: "#FFD700", // Gold accent
  });
  layer.add(ratingText);

  const outOfText = new Konva.Text({
    text: "/ 5.0",
    x: 260,
    y: 1060,
    fontSize: 48,
    fontFamily: "Arial",
    fill: "#FFFFFF",
    opacity: 0.5,
  });
  layer.add(outOfText);

  // Beverage name in bold
  const nameText = new Konva.Text({
    text: data.beverage.name.toUpperCase(),
    x: 60,
    y: 1180,
    width: WIDTH - 120,
    fontSize: 52,
    fontFamily: "Arial",
    fontStyle: "bold",
    fill: "#FFFFFF",
    lineHeight: 1.2,
  });
  layer.add(nameText);

  // Location and other details...
  // Similar structure to minimal template but with bolder styling
};
