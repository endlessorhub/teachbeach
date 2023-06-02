<template>
    <div class="social-sign-in">

        <!-- facebook sign in button -->
    <div class="signup-facebook mx-auto">
        
            <div id="fb-root"></div>
            <div class="facebook-signup" @click.prevent="loginWithFacebook">
                <div class="image">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="#3578E5"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>
                </div>
              <p>Sign in with Facebook</p>
            </div>
          </div>


          <!-- google sign in button -->
          <div class="mx-auto">
            <div id="google-sign-in" data-logo_alignment="left">
            google</div>
            </div>
            </div>
</template>
<script>
import {mapActions} from 'vuex'
import { GoogleClientId } from '../mixins/google'
export default {
    mounted: function () {
        this.initializeGoogleLogin()
    },
    methods: {
        
        ...mapActions("socialAuth", ["facebookLogin", "googleLogin"]),
        ...mapActions(["handShake"]),
        async loginWithFacebook() {
            //gettting CSRF token
            const csrftoken = await this.handShake()
    
            window.FB.login((response) => {
                // runs when user is signed in with facebook
                if (response.status === "connected") {
                    const params = new URLSearchParams();                   
                    params.append('auth_token', response.authResponse.accessToken)
                    params.append('csrftoken', csrftoken)

                    // request backend for facebook login   
                    this.facebookLogin(params).then(() => { 
                        this.$emit('loggedIn',true)
                    })
                }
            })
        },
        async loginWithGoogle(googleUser) {
            // runs when user is signed in with google
            if (googleUser.credential) {
                //gettting CSRF token
                const csrftoken = await this.handShake()
                const params = new URLSearchParams();
                params.append('csrftoken', csrftoken)
                params.append('auth_token', googleUser.credential)

                // request backend for google login
                await this.googleLogin(params)
                this.$emit('loggedIn',true)
            }
        },
        initializeGoogleLogin() {
            window.google.accounts.id.initialize({
                client_id: GoogleClientId(),
                callback: this.loginWithGoogle
            })
            window.google.accounts.id.renderButton(
                document.getElementById('google-sign-in'),
                { theme: "filled_blue", size: "medium", logo_alignment: "left", }
            )
        },
    }
}
</script>
<style scoped>
.social-sign-in{
    display:flex;
    flex-direction:column;
    margin-bottom: 10px;
    align-items: center;
    justify-content: center;
}

.signup-facebook{
    display:flex;
    justify-content: flex-start;
    align-items: center;
    background-color:rgb(82, 188, 255);
    color:white;
    width:fit-content;
    border-radius:4px;
    padding:2px;
    font-size: 14px;
    height: 32px;
    margin: 10px auto;
    cursor: pointer;
    transition: all .3s;
}
.signup-facebook:hover {
    opacity: 0.7;
}
.signup-facebook .image {
    height: 28px;
    margin-right: 10px;
    min-width: 28px;
    width: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fff;
    border-bottom-left-radius: 3px;
    border-top-left-radius: 3px;
}
.signup-facebook .facebook-signup {
    width: 100%;
    display: flex;
    align-items: center;
}
.signup-facebook .facebook-signup p {
    font-family: system-ui;
    font-weight: 500;
    font-size: 14px;
    margin-bottom: 0;
    letter-spacing: 0.25px;
    color: #fff;
    overflow: hidden;
    text-overflow: ellipsis;
    width: fit-content;
    margin-right: 6px;
}
</style>
