<template>
  <div>
    <img :src="ogImage" alt="OG Image" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      ogImage: null,
    };
  },
  mounted() {
    this.getOGImage("https://88bamboo.co/blogs/whisky-rum-gin-vodka-distillery-spotlight/a-tranquil-distillery-famous-for-its-giraffes-the-glenmorangie-distillery"); // Call method to fetch OG image URL
  },
  methods: {
    getOGImage(url) {
      this.$axios({
        url: url.startsWith('https://88bamboo.co/') ? url.replace('https://88bamboo.co/', '/api/') : url,
        method: "get",
        headers: {
          accept: "*/*",
        },
      })
      .then((res) => {
        const html = res.data;
        const regex = /<meta property="og:image" content="([^"]+)">/;
        const match = html.match(regex);
        const url = match ? match[1] : null;
        
        this.ogImage = url;
      })
      .catch((err) => {
        console.log(err);
      });
    }

  }
};
</script>
