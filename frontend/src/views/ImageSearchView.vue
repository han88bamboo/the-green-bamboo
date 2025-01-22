<template>
    <NavBar />
        
    <div class="image-search">
        <h1>Wondering if a drink is worth a try?</h1>
        <p>Scan the drink label to discover more info!</p>
        
        <div class="greybox">
            <div class="upload-section">
              <!-- The file input is hidden -->
              <input id="file-upload" type="file" @change="onFileChange" hidden />
            
              <!-- The label is styled like a button or clickable text -->
              <img
                    src="@../../../Images/Others/camera.png"
                    alt="Camera"
                    class="camera-icon"
                    @click="onImageLinkSubmit"
                />
              <label for="file-upload" class="custom-file-upload">
                Drag an image here or upload a file.
              </label>
            </div>
            
            <div>OR</div>
            
            <div class="link-section">
                <input
                type="text"
                placeholder="Paste image link"
                v-model="imageLink"
                @keypress.enter="onImageLinkSubmit"
                />
                <img
                    src="@../../../Images/Others/search.png"
                    alt="Search"
                    class="search-icon"
                    @click="onImageLinkSubmit"
                />
            </div>
        </div>
    </div>
  </template>
  
  <script>
    import NavBar from '@/components/NavBar.vue';
    export default {
        name: 'ImageSearchView',
        components: {
            NavBar,
        },
    
    data() {
      return {
        imageLink: ''
      };
    },
    methods: {
      onFileChange(event) {
        const file = event.target.files[0];
        if (file) {
          // Handle the file upload logic here
          console.log(file);
        }
      },
      onImageLinkSubmit() {
        if (this.imageLink) {
          // Handle the image link submission logic here
          console.log(this.imageLink);
        }
      }
    }
  };
  </script>
  
  <style scoped>
    .image-search {
        text-align: center;
        margin-top: 50px;
    }
    
    .greybox {
    width: 50%;
    margin: 50px auto;
    background-color: #f4f4f47d; 
    border-radius: 5px;
    display: block;
    text-align: center;
    border:5px solid #027562;
    padding:50px 10px;
    }
    
    .upload-section,
    .link-section {
        margin: 20px auto;
        width: 80%;
    }
    
    .image-search h1,
    .image-search p {
        color: #027562; 
    }
    
    .custom-file-upload {
        display: inline-block;
        padding: 10px 20px;
        cursor: pointer;
        background-color: #f4f4f4;
        border: 2px dashed #ccc;
    }
    
    input[type="text"] {
        width: calc(100% - 50px);
        padding: 10px;
        display: inline-block;
        vertical-align: middle;
    }
    
    button {
        padding: 10px 20px;
        background-color: #027562;
        color: white;
        border: none;
        cursor: pointer;
    }

    .link-section {
    display: flex;
    align-items: center;
    justify-content: center;
    }

    .search-icon{
    width: 5%;  
    cursor: pointer;
    display: inline-block;
    vertical-align: middle;
    margin-left: 10px;
    }

    .camera-icon{
    width: 5%;  
    display: inline-block;
    vertical-align: middle;
    margin-right: 10px;
    }

  </style>
  