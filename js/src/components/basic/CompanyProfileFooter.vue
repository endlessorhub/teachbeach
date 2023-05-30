<template>
    <footer>
        <v-container>
            <v-layout>
                <v-flex lg4 class="text-xs-left">
                    <!-- <img src="@/assets/profile-company2/footer_logo.svg" class="footerLogo"> -->
                    <img src="@/assets/profile-company2/logo.png" class="footerLogo">
                    <p><a href="tel:408.892.9815">408.892.9815</a></p>
                    <p><a href="mailto:alisa@web3collab.org">alisa@web3collab.org</a></p>
                </v-flex>
                <v-flex lg2 offset-lg2 class="text-xs-left">
                    <h4>Quick Links</h4>
                    <ul>
                        <li v-if="companyProfile && companyProfile.about_us_url"><a :href="companyProfile.about_us_url">About Us</a></li>
                        <li><router-link :to="'/company_classes/group/'+companySlug">Courses & Events</router-link></li>
                        <li>Private instructors</li>
                        <li @click="buyMembership" style="cursor: pointer;">Become an instructor</li>
                    </ul>
                </v-flex>
            </v-layout>
            <div class="hrdiv"></div>
            <div class="footer_copyright">
                <v-layout>
                    <v-flex lg6 class="text-xs-left">
                        <p>© Copyrights 2022</p>
                    </v-flex>
                    <v-flex lg6 class="text-xs-right">
                        <ul>
                            <li>
                                <a href="#"><img src="@/assets/profile-company2/facebook.svg" alt="facebook"></a>
                            </li>
                            <li>
                                <a href="#"><img src="@/assets/profile-company2/linkedin.svg" alt="linkedin"></a>
                            </li>
                            <li>
                                <a href="#"><img src="@/assets/profile-company2/instagram.svg" alt="instagram"></a>
                            </li>
                        </ul>
                    </v-flex>
                </v-layout>
            </div>
        </v-container>
    </footer>
</template>
<script>
export default {
    props: {
        companySlug: [Number, String],
        companyProfile: Object,
    },
    methods: {
        buyMembership() {
            this.$router.push(`/company/membership/${this.companySlug}?return=${this.$route.path}`)
        },
    }
}
</script>
<style scoped lang="scss">

body .company-profile-page {
    background: #FFFFFF;
    font-family: 'Poppins', sans-serif;
}

.collapse{
    display: flex;
    justify-content: flex-end;
}
.join_btn {
    float: right;
}
.main-info .join_btn {
    float: left;
}
a.logo_img{
    margin-right: 146px;
}
section.header{
    height: 140px;
}
.main-info {
    background-color: #F8F8F8;
    padding-top: 20px;
    padding-bottom: 20px;
}
.main-info .content {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.main-info .caption h1{
    font-size: 55px;
    color: #2B2B2B;
    font-weight: 600;
    line-height: 60px;
    margin-bottom: 23px;
}
.main-info .caption h1 span{
    color: #4EA42F;
    text-decoration: underline;
}
.main-info .description p{
    margin-bottom: 23px;
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 28px;
    color: #575757;
}
.btn_btn{
    position: relative;
    width: 192px;
    height: 39px;
    border: none;
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #FFFFFF;
    background: #4EA42F;
    border-radius: 27px;
    justify-content: center;
    align-items: center;
    display: flex;
}

.f_image{
    width: 75%;
    height: auto;
    float: right;
}
.classes {
    padding-top: 10px;
}
.classes .caption{
    margin-bottom: 15px;
}
.classes .caption h2{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 700;
    font-size: 38px;
    line-height: 38px;
    text-align: left;
    color: #999999;
}
.classes .caption p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 22.53px;
    line-height: 26px;
    text-align: center;
    color: #575757;
}
.classes .classes-carousel .item {
    overflow: hidden;
    border-radius: 12px;
    border: 1.18438px solid #F2EFEF;

    .class-desc {
        max-height: 1.3em;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 1em;
        padding: 0;
        text-align: left;
    }
}
.classes .classes-carousel{
    position: relative;
}
.classes .classes-carousel .owl-prev{
    position: absolute;
    top: 45%;
    left: -50px;
}
.classes .classes-carousel .owl-next{
    position: absolute;
    top: 45%;
    right: -50px;
}

.classes .classes-carousel .item .img{
    width: 100%;
    height: 180px;
}
.classes .classes-carousel .item .border-blue{
    width: 100%;
    height: 5px;
    background: linear-gradient(175.6deg, #0E6BA8 -25.14%, #155799 107.01%);
}
.classes .classes-carousel .item .text-content{
    padding: 20px 0 0 18px;
}
.classes .classes-carousel .item .text-content h4{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #2B2B2B;
    margin-bottom: 13px;
}
.classes .classes-carousel .item .text-content label{
    font-family: 'Open Sans';
    font-style: italic;
    font-weight: 400;
    font-size: 14px;
    line-height: 14px;
    color: #575757;
    width: 100%;
    margin-bottom: 20px;
    display: inline-block;
    box-sizing: border-box;
    text-align: left;
}
.classes .classes-carousel .item .text-content a{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 16.5813px;
    line-height: 21px;
    color: #2B2B2B;
    display: flex;
    margin-bottom: 20px;
}
.classes .classes-carousel .item .text-content a .img{
    width: 16px;
    height: auto;
    padding-left: 8px;
}
.classes .join-classes {
    float: right;
    width: 402px;
    background: #797979;
}

.mentors {
    padding-top: 83px;
}
.mentors .caption{
    margin-bottom: 65px;
}
.mentors .caption h2{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 700;
    font-size: 38px;
    line-height: 38px;
    text-align: left;
    color: #999999;
    margin-bottom: 20px;
}
.mentors .caption h2 span{
    color: #4EA42F;
}
.mentors .caption p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 16px;
    text-align: left;
    color: #575757;
}
.mentors  .mentors-carousel .owl-nav{
    margin-top: 19px;
}
.mentors  .mentors-carousel .owl-prev{
    position: absolute;
    left: 46%;
}
.mentors  .mentors-carousel .owl-next{
    position: absolute;
    right: 46%;
}

.mentors .mentors-carousel .item .img{
    border-radius: 50%;
}
.mentors .mentors-carousel .item .text-content{
    padding: 15px 0;
    position: relative;
}
.mentors .mentors-carousel .item .text-content img{
    position: absolute;
    top: -200px;
    right: -10px;
    width: 40px;
    height: 40px;
}
.mentors .mentors-carousel .item .text-content h4{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 22px;
    color: #2B2B2B;
    text-align: center;
}
.mentors .mentors-carousel .item .text-content p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #155799;
    text-align: center;
}
.mentors .joinButton {
    padding-top: 90px;
    width: 192px;
    margin: 0 auto;
}
.join-us {
    padding-top: 65px;
}
.join-us .join-us-bg {
    position: relative;
    background: #797979;
    border-radius: 40px;
    padding: 53px 98px 69px 98px;
}


.join-us .join-us-bg h2{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 700;
    font-size: 36px;
    line-height: 44px;
    color: #FFFFFF;    
}
.join-us .join-us-bg .joinusbtn{
    display: none;
}
.inputText, .inputEmail, .selectClass{
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    border: none;
    width: 100%;
    height: 39px;
    padding: 10px 15px;
    margin-bottom: 20px;
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #575757;    
    z-index: 1111;
    position: relative;
}
.inputText:focus-visible, .inputEmail:focus-visible, .selectClass:focus-visible, .inputMessage:focus-visible{
    outline: none;
}
.inputText::placeholder, .inputEmail::placeholder, .selectClass::placeholder, .inputMessage::placeholder{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #575757;
}

.inputMessage{
    background: rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    border: none;
    width: 100%;
    height: 70px;
    padding: 10px 15px;
}

@media only screen and (max-width: 1280px){
    .main-info .caption h1 {
        font-size: 50px;
        line-height: 80px;
    }
    .main-info .description p {
        font-size: 17px;
    }
    .f_image {
        width: 80%;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 50px;
    }
    .classes .caption p, .mentors .caption p{
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content h4 {
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content label {
        font-size: 14px;
    }
    .classes .classes-carousel .item .text-content a {
        font-size: 13px;
    }
    .join-us .join-us-bg h2 {
        font-size: 34px;
    }
}
@media only screen and (max-width: 1024px) {
    a.logo_img {
        margin-right: 0px;
    }
    .main-info .caption h1 {
        font-size: 50px;
        line-height: 70px;
    }
    .main-info .description p {
        font-size: 17px;
    }
    .f_image {
        width: 100%;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 40px;
    }
    .classes .caption p, .mentors .caption p {
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content h4 {
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content label {
        font-size: 13px;
    }
    .classes .classes-carousel .item .text-content a {
        font-size: 12px;
    }
    .classes .joinButton {
        padding-top: 45px;
    }
    .mentors .mentors-carousel .item .text-content {
        padding: 15px 0 0 15px;
        position: relative;
    }
    .mentors .mentors-carousel .item .text-content h4 {
        font-size: 15px;
    }
    .mentors .mentors-carousel .item .text-content p {
        font-size: 12px;
    }
    .mentors .mentors-carousel .owl-prev {
        position: absolute;
        left: 44%;
    }
    .mentors .mentors-carousel .owl-next {
        position: absolute;
        right: 44%;
    }
    .mentors .joinButton {
        padding-top: 70px;
    }
    .join-us .join-us-bg {
        padding: 53px 50px 69px 50px;
    }
    .join-us .join-us-bg h2 {
        font-size: 30px;
    }
    .join-us .join-us-bg:before, .join-us .join-us-bg:after{
        display: none;
    }
   
}

@media only screen and (max-width: 992px) {   
    section.header {
        height: 100px;
    }

    a.logo_img {
        margin-right: 60px;
    }
    .logo_img img {
        width: 100%;
    }

    .main-info .caption h1 {
        font-size: 40px;
        line-height: 50px;
    }
    .main-info .description p {
        font-size: 16px;
        line-height: 25px;
    }
    .f_image {
        width: 100%;
        height: auto;
        margin-top: 40px;
    }
    .main-info {
        // height: 100%;
    }
    .classes {
        padding-top: 30px;
    }
    .classes .caption {
        margin-bottom: 40px;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 35px;
    }
    .classes .caption p, .mentors .caption p {
        font-size: 16px;
    }    
    .classes .joinButton {
        padding-top: 25px;
    }
    .owl-nav {
        display: none;
    }
    .owl-dots {
        text-align: center;
    }
    .no-js .owl-carousel, .owl-carousel.owl-loaded .owl-dots {
        margin-top: 30px;
    }
    .owl-dots .owl-dot {
        margin: 5px;
    }
    button.owl-dot span {
        height: 15px;
        width: 15px;
        background-color: transparent;
        border: 1px solid #4ea42f;
        display: block;
        border-radius: 10px;
    }
    button.owl-dot.active span {
        background-color: #4ea42f;
    }
    .mentors .joinButton {
        padding-top: 45px;
    }
    .join-us .join-us-bg {
        border-radius: 20px;
        padding: 25px;
    }
    .join-us .join-us-bg:before, .join-us .join-us-bg:after {
        display: none;
    }
    .join-us .join-us-bg h2 {
        font-size: 35px;
        line-height: 40px;
        margin-bottom: 30px;
    }
    .join-us .join-us-bg .joinusbtn{
        display: flex;
        margin-top: 20px;
        justify-content: center;
    }
    .join-us .join-us-bg .join-us-btn{
        display: none;
    }
    .mentors .mentors-carousel .item .text-content img {
        top: -310px;
        right: 10px;
    }
    footer {
        margin-top: -174px;
        padding: 229px 0 20px 0;
    }
    footer h4 {
        padding-top: 20px;
    }
    button:focus:not(:focus-visible){
        box-shadow: none;
    }
}

@media only screen and (max-width: 767px) {
    section.header {
        height: 70px;
    }
    a.logo_img {
        margin-right: 60px;
    }
    .logo_img img {
        width: 100%;
    }
    .main-info .caption h1 {
        font-size: 35px;
        line-height: 40px;
    }
    .main-info .caption h1 br{
        display: none;
    }
    .main-info .description p {
        font-size: 14px;
        line-height: 20px;
    }
    .f_image {
        width: 100%;
        height: auto;
        margin-top: 40px;
    }
    .main-info {
        // height: 100%;
    }
    .classes {
        padding-top: 30px;
    }
    .classes .caption {
        margin-bottom: 40px;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 30px;
    }
    .classes .caption p, .mentors .caption p {
        font-size: 14px;
    }    
    .classes .joinButton {
        padding-top: 25px;
    }
    .owl-nav {
        display: none;
    }
    .owl-dots {
        text-align: center;
    }
    .no-js .owl-carousel, .owl-carousel.owl-loaded .owl-dots {
        margin-top: 30px;
    }
    .owl-dots .owl-dot {
        margin: 5px;
    }
    button.owl-dot span {
        height: 15px;
        width: 15px;
        background-color: transparent;
        border: 1px solid #4ea42f;
        display: block;
        border-radius: 10px;
    }
    button.owl-dot.active span {
        background-color: #4ea42f;
    }
    .mentors .joinButton {
        padding-top: 45px;
    }
    .join-us .join-us-bg {
        border-radius: 20px;
        padding: 25px;
    }
    .join-us .join-us-bg:before, .join-us .join-us-bg:after {
        display: none;
    }
    .join-us .join-us-bg h2 {
        font-size: 30px;
        line-height: 35px;
        margin-bottom: 30px;
    }
    .join-us .join-us-bg .joinusbtn{
        display: flex;
        margin-top: 20px;
        justify-content: center;
    }
    .join-us .join-us-bg .join-us-btn{
        display: none;
    }
    .mentors .mentors-carousel .item .text-content img {
        top: -240px;
        right: 10px;
    }
    footer {
        margin-top: -174px;
        padding: 229px 0 20px 0;
    }
    footer h4 {
        padding-top: 20px;
    }
}

@media only screen and (min-width: 531px) and (max-width: 766px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -460px;
        right: 10px;
    }
}

@media only screen and (min-width: 481px) and (max-width: 530px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -443px;
        right: 10px;
    }
}

@media only screen and (min-width: 461px) and (max-width: 480px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -413px;
        right: 10px;
    }
}

@media only screen and (min-width: 401px) and (max-width: 460px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -380px;
        right: 10px;
    }
}

@media only screen and (min-width: 360px) and (max-width: 400px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -330px;
        right: 10px;
    }
}
.class-image {
    width: 100%;
    height: 180px;
}
.owl-carousel .owl-nav button.owl-next, .owl-carousel .owl-nav button.owl-prev, .owl-carousel button.owl-dot {
    background: 0 0;
    color: inherit;
    border: none;
    padding: 0!important;
    font: inherit;
}
.owl-carousel .owl-dot, .owl-carousel .owl-nav .owl-next, .owl-carousel .owl-nav .owl-prev {
    cursor: pointer;
    user-select: none;
}
.classes .owl-prev {
    position: absolute;
    top: 45%;
    left: -50px;
}
.classes .owl-next {
    position: absolute;
    top: 45%;
    right: -50px;
}
.teacher-container {
    padding: 10px;

    &__link {
        font-size: 22px;
    }
}
.footer-container {
    display: flex;
    flex: row wrap;
}
footer {
    background-color: #383838;
    margin-top: -134px;
    padding: 229px 0 64px 0;

    a {
        font-family: "Poppins";
        font-style: normal;
        font-weight: 500;
        font-size: 14px;
        line-height: 18px;
        color: #fff;
    }
}
footer img.footerLogo{
    width: 50%;
    padding-bottom: 30px;
}
footer p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #FFFFFF;
}
footer h4 {
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #FFFFFF;
    padding-bottom: 20px;
}
footer ul {
    padding: 0;
}
footer ul li {
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 18px;
    color: #FFFFFF;
    padding-bottom: 10px;
    list-style: none;
}
footer .hrdiv {
    border-bottom: 1px solid #BBBBBB;
    padding-top: 29px;
}
footer .footer_copyright p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #FFFFFF;
    padding-top: 30px;
}
footer .footer_copyright ul {
    padding-top: 30px;
    float: right;
    margin-bottom: 0;
}
footer .footer_copyright ul li {
    display: inline-block;
    padding-left: 20px;
    padding-bottom: 0;
}
footer .footer_copyright ul li img {
    padding-bottom: 0;
}

</style>