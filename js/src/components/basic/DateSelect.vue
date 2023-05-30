<template>
<v-menu
    class="date-select"
    ref="menu"
    v-model="tRootMenu"
    :close-on-content-click="false"
    :nudge-right="40"
    :return-value.sync="date"
    lazy
    transition="scale-transition"
    offset-y
    full-width
    max-width="290px"
    min-width="290px"
    :disabled="$attrs.disabled"
>
    <v-text-field
      slot="activator"
      v-model="date"
      :label="label"
      :prepend-icon="showIcon ? access_date : ''"
      readonly
      :class="{'v-input--is-disabled': $attrs.disabled}"
      :disabled="$attrs.disabled"
      :error-messages="$attrs['error-messages']"
    ></v-text-field>
    <v-date-picker
      v-if="tRootMenu && !$attrs.disabled"
      v-model="date"
      full-width
      @input="$refs.menu.save(date)"
      :min="min"
      :max="max"
    ></v-date-picker>
</v-menu>
</template>

<script>
import _ from 'lodash'

import axios from 'axios'

export default {
    props: {
        date: {
            type: String,
            default: null
        },
        label: {
            type: String,
            default: 'Pick date'
        },
        showIcon: {
            type: Boolean,
            default: true
        },
        min: String,
        max: String,
        value: String,
    },

    created() {
        console.log(this)
        this.date = this.value
    },

    watch: {
        date() {
            this.$emit('change', this.date)
        }
    },

    data: () => ({
        tRootMenu: false,
    }),

    computed: {

    },

    methods: {

    }
}
</script>

<style lang="scss">
.date-select {
    &[disabled] {
        .date-select__input {
            cursor: not-allowed;
        }
    }
}

</style>