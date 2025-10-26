// composables/useKonvaShare.js
import { ref } from "vue";
import Konva from "konva";

export const useKonvaShare = () => {
  const stage = ref(null);
  const layer = ref(null);

  const initStage = (container) => {
    stage.value = new Konva.Stage({
      container: container,
      width: 1080,
      height: 1920,
    });

    layer.value = new Konva.Layer();
    stage.value.add(layer.value);

    return { stage: stage.value, layer: layer.value };
  };

  const exportToPNG = async () => {
    if (!stage.value) return null;

    const dataURL = stage.value.toDataURL({
      mimeType: "image/png",
      quality: 1,
      pixelRatio: 3, // High DPI for mobile
    });

    return dataURL;
  };

  const downloadImage = async (filename) => {
    const dataURL = await exportToPNG();

    const link = document.createElement("a");
    link.download = filename;
    link.href = dataURL;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return {
    initStage,
    exportToPNG,
    downloadImage,
    stage,
    layer,
  };
};
