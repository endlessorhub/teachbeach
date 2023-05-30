<template>
    <v-img v-bind="$attrs" :src="thumbFilename"></v-img>
</template>

<script>
import classHelper from '@/lib/helpers/Class'

export default {
    props: {
        src: null
    },
    computed: {
        thumbFilename() {
            return classHelper.isPreviewImageSrc(this.src) ? this.src : classHelper.previewImageSrc(this.src)
        },
    },
}
</script>
