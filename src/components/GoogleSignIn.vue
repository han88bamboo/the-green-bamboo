<template>
    <div class = "center-container mt-2">
        <div id="signin_button"></div>
    </div>
</template>

<script>

    export default {
        components: {

        },
        methods: {
            handleCredentialResponse(response) {
                console.log(response);
            }
        },
        mounted: function () {
            let googleScript = document.createElement('script');
            googleScript.src = 'https://accounts.google.com/gsi/client';
            document.head.appendChild(googleScript);
            
            window.addEventListener('load', () => {
                console.log(window.google);
                window.google.accounts.id.initialize({
                    client_id: "957457826831-12kr8lvibrnc0i3rh8tnalqhnv35ar4p.apps.googleusercontent.com",
                    callback: this.handleCredentialResponse
                });
                window.google.accounts.id.renderButton(
                    document.getElementById("signin_button"),
                    { theme: "outline", size: "large" }  // customization attributes
                );
            })
        }
    }
</script>

<style scoped>
.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>