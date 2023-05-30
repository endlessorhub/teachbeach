<template>
<div>
  <v-carousel
    :hide-delimiters="true"
    ref="carouselEl"
    v-if="items.length > 1"
    :height="height"
  >
        <v-carousel-item
          v-for="(item,i) in items"
          :key="i"
        >
            <v-img v-if="item.type === 'image'" :src="item.src" style="margin:auto;" :aspect-ratio="aspectRatio" />
            <div v-else-if="item.type === 'video'" :src="item.src" >supposed to be video player, disabled due to affecting bundle size too much</div>
        </v-carousel-item>
  </v-carousel>

  <v-img v-else-if="items.length === 1 && items[0].type === 'image'" :src="items[0].src" style="margin:auto;" :aspect-ratio="aspectRatio" />
    <div v-else-if="items.length === 1 && items[0].type === 'video'" :src="items[0].src" >supposed to be video player, disabled due to affecting bundle size too much</div>
</div>
</template>
<script>
//import _ from 'lodash'
//import VueCoreVideoPlayer from 'vue-core-video-player'

export default {
    name: 'basic_gallery',
    data: () => ({
        isLoading: false,
        width: 500,
        aspectRatio: 1.25,
    }),
    props: [
        'items',
    ],
    components: {
        //VueCoreVideoPlayer
    },
    created() {
        this.$nextTick(() => {
            this.updateWidth()
        })
        window.addEventListener('resize', this.updateWidth);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.updateWidth);
    },
    computed: {
        height() {
            return this.width/this.aspectRatio
        },
    },
    methods: {
        updateWidth() {
            this.width = this.$refs.carouselEl && this.$refs.carouselEl.$el && this.$refs.carouselEl.$el.clientWidth || 500
        },
    },

    watch: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>