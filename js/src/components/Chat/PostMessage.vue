<template>
    <div class="ChatContainer-MessageBox">
        <img src="../../../../image/profile.png" >
        <div class="textarea-container">
            <textarea v-model="message" placeholder="Message the group" rows="5" cols="60" >
            </textarea>
            <v-btn @click="postMessage()" class="btn"><v-icon>send</v-icon></v-btn>
        </div>
    </div>
</template>

<script>
export default {
    data: () => ({
        message:null,
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