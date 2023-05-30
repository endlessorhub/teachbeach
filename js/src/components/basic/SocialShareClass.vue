<template>
    <div class="buttons">
        <v-btn :lignt="false" :dark="false" @click="onClickFacebook" class="btn-facebook"><v-icon>fab fa-facebook</v-icon>&nbsp; Facebook</v-btn>
        <div ref="twitter" style="height: 28px;"></div>
        <v-btn :lignt="false" :dark="false" @click="onClickLinkedin" class="btn-linkedin"><v-icon>fab fa-linkedin</v-icon>&nbsp; Linkedin</v-btn>
    </div>
</template>

<script>

export default {
    props: {
        'classId': {
            type: Number,
            default: 0,
        },
        'className': {
            type: String,
            default: '',
        },
        'layout': {
            type: String,
            default: 'button',
        },
        'size': {
            type: String,
            default: 'large',
        },
    },

    components: {

    },

    computed: {
        url() {
            return `${window.location.origin}/class/${this.classId}`;
        },
        facebookUrl() {
            return `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(this.url)}`;
        },
        linkedinUrl() {
            return `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(this.url)}&title=${this.className}`;
        },
    },

    mounted() {
        twttr.widgets.createShareButton(
            this.url,
            this.$refs.twitter,
            {
                text: this.className,
                size: this.size,
            }
        );
    },

    methods: {
        onClickFacebook() {
            window.open(this.facebookUrl);
        },
        onClickLinkedin() {
            window.open(this.linkedinUrl);
        },
    },

    watch: {

    }
}
</script>

<style scoped lang="scss">
@mixin btn() {
    border-radius: 4px;
    font-size: 13px;
    height: 28px;
    padding: 0 8px;
    background: #1877f2 !important;
    border: 0;
    color: #fff;
    cursor: pointer;
}
h4 {
    text-align: center;
}
.btn-facebook {
    @include btn();
}
.btn-linkedin {
    @include btn();
}
.buttons {
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    align-items: center;
}
</style>