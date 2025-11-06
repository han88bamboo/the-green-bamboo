// composables/useKonvaShare.js
import { ref } from "vue";
import Konva from "konva";

export const useKonvaShare = () => {
  const stage = ref(null);
  const backgroundLayer = ref(null);
  const contentLayer = ref(null);

  const initStage = (container, dimensions) => {
    stage.value = new Konva.Stage({
      container: container,
      width: dimensions.width,
      height: dimensions.height,
    });

    backgroundLayer.value = new Konva.Layer({ name: "background" });
    contentLayer.value = new Konva.Layer({ name: "content" });

    stage.value.add(backgroundLayer.value);
    stage.value.add(contentLayer.value);

    return {
      stage: stage.value,
      backgroundLayer: backgroundLayer.value,
      contentLayer: contentLayer.value,
    };
  };

  const exportToPNG = async () => {
    if (!stage.value) return null;

    // Hide background for transparent export
    if (backgroundLayer.value) {
      backgroundLayer.value.hide();
      stage.value.draw(); // Redraw to apply changes
    }

    const dataURL = stage.value.toDataURL({
      mimeType: "image/png",
      quality: 1,
      pixelRatio: 2,
    });

    // Restore background for preview
    if (backgroundLayer.value) {
      backgroundLayer.value.show();
      stage.value.draw();
    }

    return dataURL;
  };

  const downloadImage = async (filename) => {
    const dataURL = await exportToPNG();

    if (dataURL) {
      const link = document.createElement("a");
      link.download = filename;
      link.href = dataURL;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return {
    initStage,
    exportToPNG,
    downloadImage,
    stage,
    backgroundLayer,
    contentLayer,
  };
};
