<!-- ShareCardGenerator.vue -->
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useKonvaShare } from '@/composables/ShareCard/useKonvaShare'
import { useImageLoader } from '@/composables/ShareCard/useImageLoader'
import { createMinimalTemplate } from './templates/MinimalTemplate'
import { createBoldTemplate } from './templates/BoldTemplate'

const props = defineProps({
  reviewData: {
    type: Object,
    required: true
  },
  template: {
    type: String,
    default: 'minimal'
  }
})

const emit = defineEmits(['close', 'copy-link'])

const containerRef = ref(null)
const isGenerating = ref(false)
const previewUrl = ref(null)
const error = ref(null)

const { initStage, downloadImage, layer, stage } = useKonvaShare()
const { loadMultipleImages } = useImageLoader()

const templates = {
  minimal: createMinimalTemplate,
  bold: createBoldTemplate
}

const generateCard = async () => {
  if (!containerRef.value) {
    console.error('Container ref not available')
    return
  }

  isGenerating.value = true
  error.value = null

  try {
    // Initialize Konva stage with explicit dimensions
    const { layer: konvaLayer } = initStage(containerRef.value, {
      width: 1080,
      height: 1080
    })

    // Preload all images
    const imagesToLoad = []
    if (props.reviewData.beverage?.image) {
      imagesToLoad.push(props.reviewData.beverage.image)
    }
    if (props.reviewData.user?.avatar) {
      imagesToLoad.push(props.reviewData.user.avatar)
    }

    const loadedImages = await loadMultipleImages(imagesToLoad)

    const images = {
      beverage: loadedImages[0] || null,
      avatar: loadedImages[1] || null
    }

    // Normalize review data to ensure rating is a number
    const normalizedData = {
      ...props.reviewData,
      review: {
        ...props.reviewData.review,
        rating: Number(props.reviewData.review?.rating) || 0
      }
    }

    // Render selected template
    const templateFn = templates[props.template]
    if (!templateFn) {
      throw new Error(`Template ${props.template} not found`)
    }

    await templateFn(konvaLayer, normalizedData, images)

    // Wait for next tick to ensure rendering is complete
    await new Promise(resolve => setTimeout(resolve, 100))

    // Generate preview
    if (stage.value) {
      previewUrl.value = stage.value.toDataURL({
        mimeType: 'image/png',
        quality: 1,
        pixelRatio: 2,
        fill: null,
      })
      console.log('Preview generated:', previewUrl.value ? 'Success' : 'Failed')
    } else {
      throw new Error('Stage not initialized')
    }
  } catch (err) {
    console.error('Error generating card:', err)
    error.value = err.message || 'Failed to generate card'
  } finally {
    isGenerating.value = false
  }
}

const handleDownload = async () => {
  if (!stage.value) return;

  try {
    // 🔹 1. Hide background (any node with class "background")
    const bgNode = stage.value.findOne('.background');
    if (bgNode) bgNode.hide();

    // 🔹 2. Export stage as PNG without background fill
    const dataURL = stage.value.toDataURL({
      mimeType: 'image/png',
      quality: 1,
      pixelRatio: 2,
      fill: null, // ✅ transparent background
    });

    // 🔹 3. Restore background after export
    if (bgNode) bgNode.show();

    // 🔹 4. Trigger download
    const filename = `${props.reviewData.beverage.name
      .replace(/\s+/g, '-')
      .toLowerCase()}-review.png`;

    // 👇 Make sure downloadImage accepts both arguments
    await downloadImage(filename, dataURL);
  } catch (error) {
    console.error('Download failed:', error);
  }
};

onMounted(() => {
  // Small delay to ensure DOM is ready
  setTimeout(() => {
    generateCard()
  }, 50)
})

watch(() => props.template, () => {
  if (layer.value) {
    layer.value.destroyChildren()
    generateCard()
  }
})
</script>

<template>
  <div class="share-card-generator">
    <!-- Template Selector -->
    <!-- <div class="template-selector">
      <button v-for="(_, templateName) in templates" :key="templateName" :class="{ active: template === templateName }"
        @click="$emit('update:template', templateName)">
        {{ templateName }}
      </button>
    </div> -->

    <!-- Konva Container (hidden, just for rendering) -->
    <div class="konva-container">
      <div ref="containerRef" />
    </div>

    <!-- Loading State -->
    <div v-if="isGenerating" class="loading">
      <div class="spinner"></div>
      <p>Generating your share card...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="generateCard" class="retry-btn">Retry</button>
    </div>

    <!-- Preview -->
    <div v-else-if="previewUrl" class="preview">
      <img :src="previewUrl" alt="Share card preview" />
    </div>

    <!-- Actions -->
    <div class="actions">
      <button @click="handleDownload" :disabled="isGenerating || !previewUrl" class="primary">
        Download Image
      </button>
      <button @click="emit('copy-link')" class="secondary">
        Copy Link
      </button>
    </div>

    <p class="hint">
      Save to camera roll, then upload to Instagram
    </p>
  </div>
</template>

<style scoped>
.share-card-generator {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.konva-container {
  position: absolute;
  left: -9999px;
  top: -9999px;
  width: 1080px;
  height: 1080px;
}

.preview {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  background: #f5f5f5;
}

.preview img {
  width: 100%;
  height: auto;
  display: block;
}

.template-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}

.template-selector button {
  padding: 10px 20px;
  border: 2px solid #ddd;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  text-transform: capitalize;
  transition: all 0.2s;
}

.template-selector button:hover {
  border-color: #667eea;
}

.template-selector button.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
  flex-wrap: wrap;
}

.actions button {
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.actions button.primary {
  background: #667eea;
  color: white;
}

.actions button.primary:hover:not(:disabled) {
  background: #5568d3;
}

.actions button.secondary {
  background: #ddd;
  color: #333;
}

.actions button.secondary:hover {
  background: #ccc;
}

.actions button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hint {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 10px;
}

.loading {
  text-align: center;
  padding: 60px 40px;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.error {
  text-align: center;
  padding: 40px;
  color: #d32f2f;
}

.retry-btn {
  margin-top: 16px;
  padding: 10px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.retry-btn:hover {
  background: #5568d3;
}
</style>
