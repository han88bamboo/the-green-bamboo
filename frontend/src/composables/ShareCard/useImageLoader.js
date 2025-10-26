// composables/useImageLoader.js

export const useImageLoader = () => {
  const loadImage = (url) => {
    return new Promise((resolve, reject) => {
      const image = new window.Image();
      image.crossOrigin = "Anonymous";

      image.onload = () => resolve(image);
      image.onerror = reject;

      image.src = url;
    });
  };

  const loadMultipleImages = async (urls) => {
    return Promise.all(urls.map((url) => loadImage(url)));
  };

  return {
    loadImage,
    loadMultipleImages,
  };
};
