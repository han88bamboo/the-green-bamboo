<template>
  <div class="quill-editor-container">
    <div class="row mb-3">
      <div class="col-12">
        <label class="form-label fw-bold">Section Title</label>
        <input 
          v-model="sectionTitle" 
          type="text" 
          class="form-control" 
          placeholder="Enter section title"
        >
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <label class="form-label fw-bold">Content</label>
        <div ref="editor" style="min-height: 200px; margin-bottom: 20px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Quill from 'quill';

export default {
  name: 'RichTextEditor',
  props: {
    initialTitle: {
      type: String,
      default: ''
    },
    initialContent: {
      type: String,
      default: ''
    }
  },
  emits: ['content-changed', 'title-changed'],
  data() {
    return {
      quill: null,
      sectionTitle: this.initialTitle
    }
  },
  mounted() {
    this.initializeEditor();
  },
  watch: {
    sectionTitle(newTitle) {
      this.$emit('title-changed', newTitle);
    },

    initialTitle(newTitle) {
      this.sectionTitle = newTitle;
    },
    
    initialContent(newContent) {
      if (this.quill && newContent !== this.quill.root.innerHTML) {
        this.quill.root.innerHTML = newContent;
      }
    }
  },
  methods: {
    initializeEditor() {
      const toolbarOptions = [
        ['bold', 'italic', 'underline'],
        ['link'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['image'],
        ['clean']
      ];

      this.quill = new Quill(this.$refs.editor, {
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

      // Set initial content
      if (this.initialContent) {
        this.quill.root.innerHTML = this.initialContent;
      }

      // Listen for content changes
      this.quill.on('text-change', () => {
        this.$emit('content-changed', this.quill.root.innerHTML);
      });
    },

    async imageHandler() {
      const input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.setAttribute('accept', 'image/png');
      input.click();

      input.onchange = async () => {
        const file = input.files[0];
        
        // Check file size (5MB limit)
        if (file.size > 5 * 1024 * 1024) {
          alert('Image must be smaller than 5MB');
          return;
        }

        // Check file format
        if (file.type !== 'image/png') {
          alert('Only PNG images are allowed');
          return;
        }

        const reader = new FileReader();
        reader.onload = async (e) => {
          const base64String = e.target.result.replace(/^data:image\/png;base64,/, '');
          
          try {
            const response = await this.$axios.post(
              `${process.env.VUE_APP_API_URL}/editProducerTextSections/uploadSectionImage`,
              { image64: base64String }
            );

            if (response.data.code === 200) {
              const range = this.quill.getSelection();
              this.quill.insertEmbed(range.index, 'image', response.data.imageUrl);
            }
          } catch (error) {
            console.error('Error uploading image:', error);
            alert('Error uploading image');
          }
        };
        reader.readAsDataURL(file);
      };
    },

    getContent() {
      return this.quill.root.innerHTML;
    },

    getTitle() {
      return this.sectionTitle;
    },

    setContent(content) {
      if (this.quill) {
        this.quill.root.innerHTML = content;
      }
    },

    setTitle(title) {
      this.sectionTitle = title;
    },

    updateContent(title, content) {
      this.sectionTitle = title;
      if (this.quill) {
        this.quill.root.innerHTML = content;
      }
    },

    clearContent() {
      this.sectionTitle = '';
      if (this.quill) {
        this.quill.root.innerHTML = '';
      }
    }
  }
}
</script>

<style>
/* Quill styles are imported automatically */
.ql-editor {
  min-height: 150px;
  max-height: 300px;
  overflow-y: auto;
}

.ql-container {
  font-size: 14px;
}

.ql-toolbar {
  border-top: 1px solid #ccc;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
}

.ql-container.ql-snow {
  border-bottom: 1px solid #ccc;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
}

/* Ensure the editor container doesn't overflow */
.quill-editor-container {
  position: relative;
  z-index: 1;
}
</style>