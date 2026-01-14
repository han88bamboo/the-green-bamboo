<template>
  <div class="inline-quill-editor-container" :class="{ 'floating-toolbar-mode': floatingToolbar }">
    <!-- Plus Button (Medium-style, shows on empty lines) -->
    <button 
      v-if="floatingToolbar && showPlusButton && isDesktop"
      type="button"
      class="plus-button"
      :style="plusButtonStyle"
      @click="toggleToolbarFromPlus"
      title="Insert content"
    >
      <i class="bi bi-plus-lg"></i>
    </button>
    
    <!-- Floating Toolbar (desktop only, when floatingToolbar prop is true) -->
    <div 
      v-if="floatingToolbar && showFloatingToolbar && isDesktop" 
      ref="floatingToolbarEl"
      class="floating-toolbar"
      :style="floatingToolbarStyle"
    >
      <!-- Text Formatting -->
      <button type="button" @mousedown.prevent="formatText('bold')" :class="{ active: activeFormats.bold }" title="Bold">
        <i class="bi bi-type-bold"></i>
      </button>
      <button type="button" @mousedown.prevent="formatText('italic')" :class="{ active: activeFormats.italic }" title="Italic">
        <i class="bi bi-type-italic"></i>
      </button>
      <button type="button" @mousedown.prevent="formatText('underline')" :class="{ active: activeFormats.underline }" title="Underline">
        <i class="bi bi-type-underline"></i>
      </button>
      <span class="toolbar-divider"></span>
      
      <!-- Alignment -->
      <button type="button" @mousedown.prevent="formatAlign('')" :class="{ active: !activeFormats.align || activeFormats.align === '' }" title="Align Left">
        <i class="bi bi-text-left"></i>
      </button>
      <button type="button" @mousedown.prevent="formatAlign('center')" :class="{ active: activeFormats.align === 'center' }" title="Align Center">
        <i class="bi bi-text-center"></i>
      </button>
      <button type="button" @mousedown.prevent="formatAlign('right')" :class="{ active: activeFormats.align === 'right' }" title="Align Right">
        <i class="bi bi-text-right"></i>
      </button>
      <span class="toolbar-divider"></span>
      
      <!-- Link -->
      <button type="button" @mousedown.prevent="formatText('link')" :class="{ active: activeFormats.link }" title="Insert Link">
        <i class="bi bi-link-45deg"></i>
      </button>
      <span class="toolbar-divider"></span>
      
      <!-- Lists -->
      <button type="button" @mousedown.prevent="formatList('ordered')" :class="{ active: activeFormats.listOrdered }" title="Ordered List">
        <i class="bi bi-list-ol"></i>
      </button>
      <button type="button" @mousedown.prevent="formatList('bullet')" :class="{ active: activeFormats.listBullet }" title="Bullet List">
        <i class="bi bi-list-ul"></i>
      </button>
      <span class="toolbar-divider"></span>
      
      <!-- Image -->
      <button type="button" @mousedown.prevent="imageHandler()" title="Insert Image">
        <i class="bi bi-image"></i>
      </button>
      <span class="toolbar-divider"></span>
      
      <!-- Clear Formatting -->
      <button type="button" @mousedown.prevent="clearFormatting()" title="Clear Formatting">
        <i class="bi bi-eraser"></i>
      </button>
    </div>
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
    },
    floatingToolbar: {
      type: Boolean,
      default: false
    }
  },
  emits: ['content-changed'],
  data() {
    return {
      isContentSet: false, // Track if initial content has been set
      showFloatingToolbar: false,
      floatingToolbarStyle: {
        top: '0px',
        left: '0px'
      },
      showPlusButton: false,
      plusButtonStyle: {
        top: '0px',
        left: '0px'
      },
      currentLineIndex: 0,
      activeFormats: {
        bold: false,
        italic: false,
        underline: false,
        header: false,
        blockquote: false,
        align: '',
        link: false,
        listOrdered: false,
        listBullet: false
      },
      isDesktop: false
    }
  },
  created() {
    this.quill = null; // Plain variable, not reactive
  },
  mounted() {
    this.$nextTick(() => {
      this.initializeEditor();
    });
    
    // Check if desktop and listen for resize
    this.checkIsDesktop();
    window.addEventListener('resize', this.checkIsDesktop);
  },
  beforeUnmount() {
    if (this.quill) {
      this.quill.off('text-change');
      this.quill.off('selection-change');
      this.quill = null;
    }
    window.removeEventListener('resize', this.checkIsDesktop);
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

      // Determine toolbar config based on floating mode and screen size
      const useFloatingToolbar = this.floatingToolbar && window.innerWidth >= 992;
      
      // Create Quill instance
      this.quill = new Quill(editorRef, {
        theme: 'snow',
        modules: {
          toolbar: useFloatingToolbar ? false : {
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

      // Listen for selection changes (for floating toolbar)
      if (this.floatingToolbar) {
        this.quill.on('selection-change', this.handleSelectionChange);
      }

      // Initial height adjustment
      this.$nextTick(() => {
        this.adjustHeight();
      });
    },

    // ==========================================
    // Floating Toolbar Methods
    // ==========================================
    
    checkIsDesktop() {
      this.isDesktop = window.innerWidth >= 992;
      // Hide floating toolbar if we switch to mobile
      if (!this.isDesktop) {
        this.showFloatingToolbar = false;
      }
    },

    handleSelectionChange(range) {
      if (!this.floatingToolbar || !this.isDesktop) return;
      
      if (range && range.length > 0) {
        // Text is selected - show toolbar, hide plus button
        this.showPlusButton = false;
        this.updateActiveFormats();
        this.positionFloatingToolbar();
        this.showFloatingToolbar = true;
      } else if (range) {
        // Cursor position changed (no selection)
        this.showFloatingToolbar = false;
        this.currentLineIndex = range.index;
        this.checkAndShowPlusButton();
      } else {
        // No selection - hide both
        this.showFloatingToolbar = false;
        this.showPlusButton = false;
      }
    },

    checkAndShowPlusButton() {
      if (!this.quill) return;
      
      const range = this.quill.getSelection();
      if (!range) return;
      
      // Get the current line
      const [line] = this.quill.getLine(range.index);
      if (!line) return;
      
      // Check if line is empty (only contains newline or is blank)
      const lineText = line.domNode.textContent || '';
      const isEmpty = lineText.trim() === '' || lineText === '\n';
      
      if (isEmpty) {
        // Position plus button at the current line
        this.positionPlusButton(range.index);
        this.showPlusButton = true;
      } else {
        this.showPlusButton = false;
      }
    },

    positionPlusButton(index) {
      if (!this.quill) return;
      
      const bounds = this.quill.getBounds(index);
      const editorEl = this.$refs['editor-' + this.sectionId];
      if (!editorEl) return;
      
      const editorRect = editorEl.getBoundingClientRect();
      
      // Position button in left margin
      const top = editorRect.top + bounds.top + window.scrollY;
      const left = editorRect.left - 50 + window.scrollX; // 50px left of editor
      
      this.plusButtonStyle = {
        top: `${top}px`,
        left: `${left}px`
      };
    },

    toggleToolbarFromPlus() {
      if (!this.quill) return;
      
      // Hide plus button
      this.showPlusButton = false;
      
      // Focus the editor at current line
      this.quill.setSelection(this.currentLineIndex, 0);
      
      // Show toolbar at the current line position
      const bounds = this.quill.getBounds(this.currentLineIndex);
      const editorEl = this.$refs['editor-' + this.sectionId];
      if (!editorEl) return;
      
      const editorRect = editorEl.getBoundingClientRect();
      
      const toolbarWidth = 420;
      const toolbarHeight = 40;
      
      let left = editorRect.left + bounds.left + (bounds.width / 2) - (toolbarWidth / 2);
      let top = editorRect.top + bounds.top - toolbarHeight - 10 + window.scrollY;
      
      // Boundary detection
      const padding = 10;
      if (left < padding) left = padding;
      if (left + toolbarWidth > window.innerWidth - padding) {
        left = window.innerWidth - toolbarWidth - padding;
      }
      
      if (top < padding + window.scrollY) {
        top = editorRect.top + bounds.bottom + 10 + window.scrollY;
      }
      
      this.floatingToolbarStyle = {
        top: `${top}px`,
        left: `${left}px`
      };
      
      this.updateActiveFormats();
      this.showFloatingToolbar = true;
    },

    updateActiveFormats() {
      if (!this.quill) return;
      const format = this.quill.getFormat();
      this.activeFormats = {
        bold: !!format.bold,
        italic: !!format.italic,
        underline: !!format.underline,
        header: format.header || false,
        blockquote: !!format.blockquote,
        align: format.align || '',
        link: !!format.link,
        listOrdered: format.list === 'ordered',
        listBullet: format.list === 'bullet'
      };
    },

    positionFloatingToolbar() {
      if (!this.quill) return;
      
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      
      // Calculate toolbar position (centered above selection)
      const toolbarWidth = 420; // Width for all toolbar buttons
      const toolbarHeight = 40;
      
      let left = rect.left + (rect.width / 2) - (toolbarWidth / 2);
      let top = rect.top - toolbarHeight - 10; // 10px gap above selection
      
      // Boundary detection - keep within viewport
      const padding = 10;
      if (left < padding) left = padding;
      if (left + toolbarWidth > window.innerWidth - padding) {
        left = window.innerWidth - toolbarWidth - padding;
      }
      
      // If toolbar would go above viewport, show below selection instead
      if (top < padding) {
        top = rect.bottom + 10;
      }
      
      this.floatingToolbarStyle = {
        top: `${top}px`,
        left: `${left}px`
      };
    },

    formatText(format) {
      if (!this.quill) return;
      
      if (format === 'link') {
        const currentFormat = this.quill.getFormat();
        if (currentFormat.link) {
          this.quill.format('link', false);
        } else {
          const url = prompt('Enter link URL:');
          if (url) {
            this.quill.format('link', url);
          }
        }
      } else if (format === 'blockquote') {
        const currentFormat = this.quill.getFormat();
        this.quill.format('blockquote', !currentFormat.blockquote);
      } else {
        const currentFormat = this.quill.getFormat();
        this.quill.format(format, !currentFormat[format]);
      }
      
      this.updateActiveFormats();
    },

    formatHeader(level) {
      if (!this.quill) return;
      const currentFormat = this.quill.getFormat();
      this.quill.format('header', currentFormat.header === level ? false : level);
      this.updateActiveFormats();
    },

    formatAlign(alignment) {
      if (!this.quill) return;
      this.quill.format('align', alignment || false);
      this.updateActiveFormats();
    },

    formatList(listType) {
      if (!this.quill) return;
      const currentFormat = this.quill.getFormat();
      // Toggle list off if already that type, otherwise set it
      if (currentFormat.list === listType) {
        this.quill.format('list', false);
      } else {
        this.quill.format('list', listType);
      }
      this.updateActiveFormats();
    },

    clearFormatting() {
      if (!this.quill) return;
      const range = this.quill.getSelection();
      if (range) {
        this.quill.removeFormat(range.index, range.length);
      }
      this.updateActiveFormats();
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

/* =====================================================================================
   FLOATING TOOLBAR STYLES (Desktop only, when floatingToolbar prop is true)
   ===================================================================================== */

/* Hide default toolbar on desktop when in floating mode */
@media (min-width: 992px) {
  .floating-toolbar-mode .auto-expand-editor :deep(.ql-toolbar) {
    display: none !important;
  }
  
  .floating-toolbar-mode .auto-expand-editor :deep(.ql-container.ql-snow) {
    border-top: 1px solid #ccc !important;
    border-radius: 4px !important;
  }
}

/* Floating Toolbar */
.floating-toolbar {
  position: fixed;
  z-index: 1050;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 8px;
  background: #1a1a1a;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  animation: floatIn 0.15s ease-out;
}

@keyframes floatIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.floating-toolbar button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  background: transparent;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.floating-toolbar button:hover {
  background: rgba(255, 255, 255, 0.15);
}

.floating-toolbar button.active {
  background: rgba(255, 255, 255, 0.25);
  color: #4dabf7;
}

.floating-toolbar button i {
  font-size: 1rem;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background: rgba(255, 255, 255, 0.2);
  margin: 0 4px;
}

/* =====================================================================================
   PLUS BUTTON (Medium-style, appears in left margin on empty lines)
   ===================================================================================== */

.plus-button {
  position: fixed;
  z-index: 1049;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border: 1px solid #ddd;
  background: #fff;
  color: #999;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.plus-button:hover {
  border-color: #999;
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.plus-button i {
  font-size: 1.1rem;
  font-weight: 600;
}
</style>