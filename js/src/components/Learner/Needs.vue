<template>
  <form>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
            <v-textarea
                v-model="learnerNeeds"
                auto-grow
                box
                label=""
                rows="2"
            ></v-textarea>
        </v-flex>

      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'

import axios from 'axios'

export default {

    data: () => ({
        isLoading: false,
        learnerNeeds: '',
    }),

    created: function () {
        let _this = this
        if (this.$store.state.learnerData) {
            this.learnerNeeds = _this.$store.state.learnerData.learnerNeeds
        }

    },

    computed: {

    },

    methods: {
        back() {
            this.$emit('back:to:start')
            //this.$router.go(-1)
        },
        submit () {
            this.$store.commit('mergeLearnerData', {
                learnerNeeds: this.learnerNeeds,
            })
            this.$emit('next:step')
        },
        clear () {

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>