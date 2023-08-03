<template>
    <div class="ChatContainer-MessageBox">

        <img v-if="user.is_company_owner" src="../../../../image/profile.png" alt="">
        <v-icon v-else class="material-icons" style="font-size: 43px;">account_circle</v-icon>

        <div class="textarea-container">
            <textarea v-model="message" placeholder="Message the group" rows="5" cols="60" >
            </textarea>
            <v-btn @click="postMessage()" class="btn"><v-icon>send</v-icon></v-btn>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        user: {
            type: Object,
        },
    },
    data: () => ({
        message: null,
        
     }),
    methods: {
        /**
         * This emits the message to the parent component
         * 
         * @event onEnter
         * @type {String} 
         * 
         */
        postMessage() { 
            this.$emit('onEnter', this.message)
            this.message = undefined
        }
    }
}

</script>