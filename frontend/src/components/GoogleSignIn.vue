<template>
    <div class = "center-container mt-2">
        <div id="signin_button"></div>
    </div>
    <div class="text-danger fst-italic fw-bold fs-3">
        <span v-if="errorMessage">An error occurred while attempting to create account, please try again!</span>
        <span v-if="duplicateEntry">The account has already been created.</span>
    </div>
</template>

<script>
    import { jwtDecode } from "jwt-decode";

    export default {
        components: {

        },
        data() {
            return {
                // error messages
                duplicateEntry: false,
                errorMessage: false,

                base64Image:"",
            };
        },
        methods: {
            async handleCredentialResponse(response) {
                // this part handles the return response from google log in, we can access their information using jwt-decode library
                // user details include: email, email_verified, family_name, given_name, name, picture
                const userDetails = jwtDecode(response.credential);


                // create account only if it doesnt exist in the database
                const response2 = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUserByUsername/` + userDetails.email);
                await this.convertImageToBase64(userDetails.picture).then(base64String => {
                        this.base64Image = base64String // Outputs the Base64 string representation of the image
                    })

                // CHECK IF GOOGLE ACCOUNT EXISTS, IF IT DOES, UPDATE THE DATABASE IF PHOTO CHANGE, LOG IN, PUSH TO MAIN PAGE HOME
                if (response2 != null && response2.data != null && response2.data != "" && !(Array.isArray(response2.data) && response2.data.length == 0)) {
                    if(this.base64Image !== response2.data.photo){
                        let submitData2 = {
                            "userID" : response2.data.id,
                            "image64": this.base64Image,
                            "drinkChoice": response2.data.choiceDrinks,
                        }
                        await this.$axios.post(`${process.env.VUE_APP_API_URL}/editProfile/editDetails`, submitData2)
                    }
                    localStorage.setItem("88B_accID", response2.data.id);
                    localStorage.setItem("88B_accType", "user");
                    this.$router.push({path: '/'});
                }

                // IF DOESNT EXIST, CREATE A NEW ACCOUNT WITH EMAIL AS USERNAME, THEN PUSH TO MAIN PAGE HOME
                else{
                    let joinDate = new Date().toISOString();

                    // in the future, store this image in S3 bucket and then use the string
                    await this.convertImageToBase64(userDetails.picture).then(base64String => {
                        this.base64Image = base64String // Outputs the Base64 string representation of the image
                    })
                    let submitAPI =  "${process.env.VUE_APP_API_URL}/createAccount/createAccount"
                    let submitData = {
                        // pass in first name, last name, email, isadmin
                        "username": userDetails.email,
                        "displayName": userDetails.name,
                        "firstName": userDetails.given_name,
                        "lastName": userDetails.family_name,
                        "email": userDetails.email,
                        "choiceDrinks": [],
                        "drinkLists": {
                            "Drinks I Have Tried":{
                                "listDesc":"",
                                "listItems":[]
                            },
                            "Drinks I Want To Try":{
                                "listDesc":"",
                                "listItems":[]
                            }
                        },
                        "modType": [],
                        "photo": this.base64Image,
                        "hashedPassword": "googleSignIn",
                        "joinDate": joinDate,
                        "followLists": {
                            "users":[],
                            "producers":[],
                            "venues":[]
                        },
                        "birthday":"2024-07-24",
                        "isAdmin":false,
                    }
                    this.createAccount(submitAPI, submitData, userDetails);
                }
            },
            async convertImageToBase64(imageUrl) {
                try {
                    const response = await fetch(imageUrl);
                    const blob = await response.blob();

                    return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onloadend = () => {
                        const base64String = reader.result;
                        const cleanedBase64String = base64String.replace('data:', '').replace(/^.+,/, '');
                        resolve(cleanedBase64String);
                    };
                    reader.onerror = reject;
                    reader.readAsDataURL(blob);
                    });
                } catch (error) {
                    console.error("Error converting image to Base64:", error);
                }
            },

            async createAccount(submitAPI, submitData, userDetails){
                try{
                    let responseCode=0;
                    const response3 = await this.$axios.post(submitAPI, submitData)
                    .then((response)=>{
                        responseCode = response.data.code
                    })
                    .catch((error)=>{
                        console.error(error);
                        responseCode = error.response.data.code
                    });
                    if(responseCode==201){
                        // Route them in  after setting details
                        const response4 = await this.$axios.get(`${process.env.VUE_APP_API_URL}/getData/getUserByUsername/` + userDetails.email);
                        localStorage.setItem("88B_accID", response4.data.id);
                        localStorage.setItem("88B_accType", "user");
                        this.$router.push({path: '/'});
                    }else{
                        if(responseCode==400){
                            this.duplicateEntry = true // Display duplicate entry message
                        }else{
                            this.errorMessage = true // Display generic error message
                        }
                    }
                    return response3
                }
                catch(error){
                    console.error(error)
                }
                
            },
        },
        mounted: function () {
            // this creates the script where we pass in the google api script for google log in
            let googleScript = document.createElement('script');
            googleScript.src = 'https://accounts.google.com/gsi/client';
            document.head.appendChild(googleScript);

            // retrieve apikey for google log in
            const apiKey = process.env.VUE_APP_GAUTH_API_KEY;
            
            // this is where we add the event listener for the button for all the login stuff
            window.addEventListener('load', () => {
                console.log(window.google);
                window.google.accounts.id.initialize({
                    client_id: apiKey,
                    // after login, this will be called
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