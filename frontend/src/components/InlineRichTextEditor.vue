<template>
  <div class="inline-quill-editor-container">
    <div :ref="'editor-' + sectionId" class="auto-expand-editor"></div>
  </div>
</template>

<script>
import Quill from 'quill';

export default {
  name: 'InlineRichTextEditor',
  props: {
    initialContent: {
      type: String,
      default: ''
    },
    sectionId: {
      type: [String, Number],
      required: true
    }
  },
  emits: ['content-changed'],
  data() {
    return {
      isContentSet: false // Track if initial content has been set
    }
  },
  created() {
    this.quill = null; // Plain variable, not reactive
  },
  mounted() {
    this.$nextTick(() => {
      this.initializeEditor();
    });
  },
  beforeUnmount() {
    if (this.quill) {
      this.quill.off('text-change');
      this.quill = null;
    }
  },
  watch: {
    initialContent(newContent) {
      // Only set content if it's different and we haven't set it yet, or if it's empty
      if (this.quill && (!this.isContentSet || newContent === '')) {
        const currentContent = this.quill.root.innerHTML;
        if (currentContent !== newContent) {
          // Clear first, then set content to avoid duplication
          this.quill.setText('');
          if (newContent && newContent.trim() !== '') {
            this.quill.clipboard.dangerouslyPasteHTML(0, newContent);
          }
          this.isContentSet = true;
          this.adjustHeight();
        }
      }
    }
  },
  methods: {
    initializeEditor() {
      const editorRef = this.$refs['editor-' + this.sectionId];
      if (!editorRef) {
        console.error('Editor ref not found for section:', this.sectionId);
        return;
      }

      const toolbarOptions = [
        ['bold', 'italic', 'underline'],
        [{ 'align': [] }],
        ['link'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['image'],
        ['clean']
      ];

      // Create Quill instance
      this.quill = new Quill(editorRef, {
        theme: 'snow',
        modules: {
          toolbar: {
            container: toolbarOptions,
            handlers: {
              'image': this.imageHandler
            }
          }
        }
      });

      // Set initial content only once, avoiding duplication
      if (this.initialContent && this.initialContent.trim() !== '' && !this.isContentSet) {
        this.quill.clipboard.dangerouslyPasteHTML(0, this.initialContent);
        this.isContentSet = true;
      }

      // Listen for content changes
      this.quill.on('text-change', () => {
        this.$emit('content-changed', this.quill.root.innerHTML);
        this.adjustHeight();
      });

      // Initial height adjustment
      this.$nextTick(() => {
        this.adjustHeight();
      });
    },

    adjustHeight() {
      if (!this.quill) return;
      
      const container = this.quill.container.querySelector('.ql-editor');
      
      if (container) {
        // Reset height to auto to get the scroll height
        container.style.height = 'auto';
        
        // Set minimum height
        const minHeight = 150;
        const contentHeight = Math.max(container.scrollHeight, minHeight);
        
        // Apply the new height with a small buffer
        container.style.height = contentHeight + 20 + 'px';
      }
    },

    async imageHandler() {
      const input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.setAttribute('accept', 'image/png,image/jpeg,image/jpg,image/webp');
      
      input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;
        
        // Check file size (5MB limit)
        if (file.size > 5 * 1024 * 1024) {
          alert('Image must be smaller than 5MB');
          return;
        }

        // Check file format - accept PNG, JPG, JPEG, WebP
        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
          alert('Only PNG, JPG, JPEG, and WebP images are allowed');
          return;
        }

        // Get current selection
        const range = this.quill.getSelection(true);
        const index = range ? range.index : this.quill.getLength();

        const reader = new FileReader();
        reader.onload = async (e) => {
          // Strip the data URL prefix (works for any image type)
          const base64String = e.target.result.replace(/^data:image\/[a-zA-Z]+;base64,/, '');
          
          try {
            const response = await fetch(
              `${process.env.VUE_APP_API_URL}/editProducerTextSections/uploadSectionImage`,
              {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image64: base64String })
              }
            );
            const data = await response.json();

            if (data.code === 200 && data.imageUrl) {
              this.quill.insertEmbed(index, 'image', data.imageUrl);
              this.quill.setSelection(index + 1, 0);
              this.adjustHeight(); // Adjust height after image insertion
            } else {
              alert('Image upload failed');
            }
          } catch (error) {
            console.error('Error uploading image:', error);
            alert('Error uploading image');
          }
        };
        
        reader.readAsDataURL(file);
      };
      
      input.click();
    },

    getContent() {
      return this.quill ? this.quill.root.innerHTML : '';
    },

    setContent(content) {
      if (this.quill) {
        this.quill.setText(''); // Clear first
        if (content && content.trim() !== '') {
          this.quill.clipboard.dangerouslyPasteHTML(0, content);
        }
        this.adjustHeight();
      }
    },

    clearContent() {
      if (this.quill) {
        this.quill.setText('');
        this.isContentSet = false;
        this.$emit('content-changed', '');
        this.adjustHeight();
      }
    },

    focus() {
      if (this.quill) {
        this.quill.focus();
      }
    }
  }
}
</script>

<style scoped>
.inline-quill-editor-container {
  width: 100%;
}

.auto-expand-editor :deep(.ql-editor) {
  min-height: 150px;
  max-height: none; /* Remove max-height to allow expansion */
  overflow-y: auto;
  resize: none;
  padding: 15px;
  line-height: 1.6;
}

.auto-expand-editor :deep(.ql-container) {
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.auto-expand-editor :deep(.ql-toolbar) {
  border: 1px solid #ccc;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
}

.auto-expand-editor :deep(.ql-container.ql-snow) {
  border-top: none;
  border-radius: 0 0 4px 4px;
}

/* Smooth transitions for height changes */
.auto-expand-editor :deep(.ql-editor) {
  transition: height 0.2s ease;
}

/* Ensure images don't overflow */
.auto-expand-editor :deep(.ql-editor img) {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>