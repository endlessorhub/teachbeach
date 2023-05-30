<template>
    <section class="join-us">
        <v-container>
            <div class="join-us-bg">
                <v-layout>
                    <v-flex lg4>
                        <h2>Get updates from collaborators</h2>
                        <button class="btn_btn join-us-btn" @click="buyMembership">Join</button>
                    </v-flex>
                    <v-flex lg8>
                        <form name="join-us-form">
                            <v-layout wrap>
                                <v-flex lg4 md12 pr-3>
                                    <div class="input-wrapper">
                                        <input type="text" name="name" class="inputText" placeholder="Name" tabindex="1" required>
                                    </div>
                                </v-flex>
                                <v-flex lg4 md12 pr-3>
                                    <div class="input-wrapper">
                                        <input type="text" name="email" class="inputEmail" placeholder="Email" tabindex="3" required>
                                    </div>
                                </v-flex>
                                <v-flex lg4 md12>
                                    <div class="input-wrapper class-wrapper">
                                        <select name="class" class="selectClass" id="class" tabindex="5" required>
                                            <option value="" selected>Class</option>
                                            <option v-for="cl in classes" :value="cl.id">{{ cl.label }}</option>
                                        </select>
                                    </div>
                                </v-flex>
                                <v-flex lg12>
                                    <div class="form-btn-wrapper">
                                        <textarea class="inputMessage" placeholder="Message" rows="2"></textarea>
                                    </div>
                                </v-flex>
                                <v-flex lg12 class="joinusbtn">
                                    <div class="form-btn-wrapper">
                                        <button class="btn_btn" @click="buyMembership">Join</button>
                                    </div>
                                </v-flex>
                            </v-layout>
                        </form>
                    </v-flex>
                </v-layout>
            </div>
        </v-container>
    </section>
</template>
<script>
export default {
    props: {
        companySlug: [Number, String],
        companyProfile: Object,
    },
    computed: {
        classes() {
            if (!this.companyProfile) return [];
            return this.companyProfile.classes.map(v => ({
                id: v.id,
                label: v.name,
            }))
        }
    },
    methods: {
        buyMembership() {
            this.$router.push(`/company/membership/${this.companySlug}?return=${this.$route.path}`)
        },
    }
}
</script>
<style scoped lang="scss">
.join-us {
    padding-top: 65px;
}
.join-us .join-us-bg {
    position: relative;
    background: #797979;
    border-radius: 40px;
    padding: 53px 98px 69px 98px;
}
.join-us .join-us-bg:after {
    content: '';
    position: absolute;
    bottom: 50px;
    left: -40px;
    width: 97px;
    height: 115px;
    background-image: url('../../assets/profile-company2/joinUsLeft.svg');
    background-repeat: no-repeat;
}
.join-us .join-us-bg:before {
    content: '';
    position: absolute;
    top: 30px;
    right: -50px;
    width: 197px;
    height: 230px;
    background-image: url('../../assets/profile-company2/joinUsRight.svg');
    background-repeat: no-repeat;
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
.selectClass {
    appearance: none;
    background-image: url(../../assets/profile-company2/selectArrow.svg);
    background-repeat: no-repeat;
    background-position: right 15px center;
}
.inputMessage{
    background: rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    border: none;
    width: 100%;
    height: 70px;
    padding: 10px 15px;
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
.btn_btn::after{
    content: '';
    position: absolute;
    top: 6px;
    left: 6px;
    background-image: url('../../assets/profile-company2/btnIcon.svg');
    background-repeat: no-repeat;
    height: 27px;
    width: 27px;
}
</style>