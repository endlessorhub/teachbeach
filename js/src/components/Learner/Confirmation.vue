<template>
  <form>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
          <h3>Congratulations! your are enrolled for {{name}}</h3>

        </v-flex>
      </v-layout>
    </v-container>
    <v-btn color="success" @click="submit">Great!</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'

import axios from 'axios'

export default {

    props: [
        'classData'
    ],

    data: () => ({
        isLoading: false,
    }),

    created: function () {

    },

    computed: {
        name() {
            return this.classData.is_private ? this.classData.private_className : this.classData.name
        }
    },

    methods: {
        back() {
            this.$emit('prev:step')
        },
        submit () {
            this.$router.push('/dashboard/learn/classes')
            //this.$emit('next:step')
        },
        clear () {

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>