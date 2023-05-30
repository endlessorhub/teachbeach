<template>
    <GmapMap
      :center="centerPosition"
      :zoom="12"
      map-type-id="terrain"
      :style="computedStyle"
    >
        <GmapMarker
              v-if="marker && isMarkerValid"
              label=""
              :position="markerPosition"
        ></GmapMarker>
        <GmapMarker
              v-for="(marker, index) in markersPosition"
              :key="index"
              :label="marker.label"
              :position="marker.position"
              :clickable="true"
              @click="center=marker.position"
        ></GmapMarker>
    </GmapMap>
</template>

<script>
import _ from 'lodash'

export default {
    props: {
        width: '100%',
        height: '100%',
        marker: null,
        center: null,
        markers: [],
    },
    components: {

    },
    data () {
        return {
            step: 0,
        }
    },
    computed: {
        markersPosition() {
            let res = _.filter(this.markers, v => v.position && _.isFinite(v.position.lat) && _.isFinite(v.position.lng))
            return res
        },
        markerPosition() {
            return this.marker && _.isFinite(this.marker.lat) && _.isFinite(this.marker.lng) ? {lat: this.marker.lat, lng: this.marker.lng} : null
        },
        centerPosition() {
            if(this.center && _.isFinite(this.center.lat) && _.isFinite(this.center.lng)) {
                return {lat: this.center.lat, lng: this.center.lng}
            }
            if(this.marker && _.isFinite(this.marker.lat) && _.isFinite(this.marker.lng)) {
                return {lat: this.marker.lat, lng: this.marker.lng}
            }
            return {
                lat: 27.771509207197525,
                lng: -82.67681705581867
            }
        },
        computedStyle() {
            return {
                width: this.width,
                height: this.height,
            }
        },
        isMarkerValid() {
            return this.marker && _.isFinite(this.marker.lat) && _.isFinite(this.marker.lng)
        }
    },
    watch: {

    },
    methods: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>