<template>
    <v-tooltip v-model="isShown" top class="info-tooltip">
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="mapHandlers(on)">
          <v-icon color="grey lighten-1">info</v-icon>
        </v-btn>
      </template>
        <div class="info-tooltip__text"><slot></slot></div>
    </v-tooltip>
</template>

<script>

export default {
    props: {
        activatorEvent: {
            default: 'click',
            type: String,
        }
    },
    data: () => ({
        isShown: false,
    }),
    methods: {
        mapHandlers(on) {
            return this.activatorEvent === 'click' ? { click: this.onClick } : on;
        },
        onClick(event) {
            event.stopPropagation()
            this.isShown = !this.isShown
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.info-tooltip {
    &__text {
        font-size: 16px;
        width: 300px;
    }
}
</style>