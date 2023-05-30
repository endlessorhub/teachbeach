<template>
  <form>
    <v-btn @click="submit">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
          <v-flex xs12 class="text-xs-left"><h4>Nice job {{full_name}}! Now let‘s create a great profile.</h4></v-flex>
        <v-flex xs12 class="text-xs-left">
            <div class="font-weight-medium">Tips: </div>
            <ul class="caption">
                <li>Describe your background and experience</li>
                <li>How  many years in business</li>
                <li>Describe your passion for sharing and approach to teaching</li>
                <li>List educational accomplishments, relevant work and awards</li>
                <li>Include links to social profiles such as FB and LinkedIn</li>
            </ul>
        </v-flex>
        <v-flex xs12 text-xs-left>
          <div style="text-align: left;">
            <v-textarea
                v-model="description"
                auto-grow
                box
                label="What makes you stand-out as a teacher and how are you uniquely qualified?"
                rows="3"
            ></v-textarea>
            <v-combobox
              v-model="areasOfSpeciality"
              :items="specialties"
              label="Areas of speciality"
              multiple
              chips
            ></v-combobox>

          </div>
        </v-flex>

      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'

import axios from 'axios'

export default {
    props: ['alreadyRegistered', 'hasAvatar'],

    data: () => ({
        description: '',
        first_name: '',
        last_name: '',
        areasOfSpeciality: [],
        specialties: [],
    }),

    created: function () {
        let _this = this
        if (this.$store.state.profile) {
            _this.description = _this.$store.state.profile.description || ''
            _this.areasOfSpeciality = _this.$store.state.profile.areasOfSpeciality || []
        }
        if (_this.$store.state.user && Object.keys(_this.$store.state.user).length) {
            _this.first_name = _this.$store.state.user.first_name || ''
            _this.last_name = _this.$store.state.user.last_name || ''
        }
    },

    computed: {
        full_name: function () {
            return this.first_name+' '+this.last_name
        }
    },

    methods: {
        saveData() {
            this.$store.commit('setTeacherProfile', {
                description: this.description,
                areasOfSpeciality: this.areasOfSpeciality,
                last_name: this.last_name,
                first_name: this.first_name,
            })
            this.$store.commit('setTeacher', {
                description: this.description,
                areasOfSpeciality: this.areasOfSpeciality,
                last_name: this.last_name,
                first_name: this.first_name,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            this.saveData()
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