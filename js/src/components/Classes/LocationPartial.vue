<template>
  <div>
      <b>Location:</b>
      <b v-if="class_type === 'venue' && teaching_venue">{{teaching_venue}}, </b>
      <span>{{location}}</span>
      <a v-if="(class_type === 'venue' || class_type === 'address') && lat && lng" @click.stop.prevent="showMap()" :loading="isLoading" :disabled="isLoading">Map</a>
  </div>
</template>

<script>

import classHelper from '@/lib/helpers/Class.js'

export default {
    props: [
        'classData'
    ],
    computed: {
        location() {
            return classHelper.location(this.classData)
        },
    }
}
</script>

<style scoped lang="scss">

</style>