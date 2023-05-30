<template>
    <v-snackbar
      v-model="snackbar"
      color="platform-error"
      :timeout="timeout"
      top
    >
      {{ value }}
      <v-btn
        dark
        flat
        @click.stop.prevent="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>

</template>

<script>

export default {
    props: {
        value: '',
        timeout: {
            type: Number,
            default: 5000,
        }
    },

    data: () => ({

    }),

    computed: {
        snackbar: {
            get() {
                return !!this.value
            },
            set(v) {
                if(!v) {
                    this.value = ''
                }
                this.$emit('input', this.value)
            },
        },
    }
}
</script>
<style scoped lang="scss">

</style>