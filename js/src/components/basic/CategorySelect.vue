<template>
<v-select
  v-model="selected"
  :items="items"
  :label="label"
  @input="sendVal"
>
  <!--v-btn slot="label">{{label}}</v-btn-->
</v-select>
</template>

<script>
import _ from 'lodash'

export default {
    props: {
        items: Array,
        label: String,
        id: Number,
        selected: [Array, Object, Number],
        multiple: Boolean,
    },

    data: () => ({
        //select: null
    }),

    computed: {

    },

    watch: {

    },

    created: function () {
        //console.log(this, arguments)
        //this.select = this.selected
    },

    methods: {
        sendVal() {
            this.$emit('update:selection', {
                id: this.id,
                value: this.selected
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>