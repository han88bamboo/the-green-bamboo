// utils/konvaHelpers.js
import Konva from 'konva';

/**
 * Adds a gradient background to a Konva layer.
 * @param {Konva.Layer} layer The layer to add the background to.
 * @param {Array} colorStops Array of color stops, e.g., [0, '#ff0000', 1, '#0000ff'].
 * @param {number} width The width of the background.
 * @param {number} height The height of the background.
 */
export function addGradientBackground(layer, colorStops, width, height) {
  const background = new Konva.Rect({
    x: 0,
    y: 0,
    width,
    height,
    fillLinearGradientStartPoint: { x: 0, y: 0 },
    fillLinearGradientEndPoint: { x: width, y: height },
    fillLinearGradientColorStops: colorStops,
  });
  layer.add(background);
}

/**
 * Wraps a Konva.Text object's text.
 * @param {Konva.Text} textNode The text node to wrap.
 * @param {number} maxWidth The maximum width for a line.
 */
export function wrapText(textNode, maxWidth) {
    const words = textNode.text().split(' ');
    let line = '';
    let lines = '';

    for (let n = 0; n < words.length; n++) {
        const testLine = line + words[n] + ' ';
        const metrics = textNode.getLayer().getContext().measureText(testLine);
        const testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            lines += line + '\n';
            line = words[n] + ' ';
        } else {
            line = testLine;
        }
    }
    lines += line;
    textNode.text(lines);
}


/**
 * Centers a text node horizontally.
 * @param {Konva.Text} textNode The text node to center.
 * @param {number} containerWidth The width of the container to center within.
 */
export function centerText(textNode, containerWidth) {
    const textWidth = textNode.width();
    textNode.x((containerWidth - textWidth) / 2);
}