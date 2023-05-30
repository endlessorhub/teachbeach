<template>
  <form>
    <h1>{{ title }}</h1>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
          <v-radio-group v-model="whereTeach">
              <v-radio label="Address I provide" value="address" ></v-radio>
              <v-radio value="venue" >
                <div slot="label">
                  <span></span>
                  <v-select
                    :items="venues"
                    label="Select from venue list"
                    v-model="locationVenue"
                  ></v-select>
                </div>
              </v-radio>
              <v-radio v-if="classType == 'private'" label="Student’s location" value="student_location" ></v-radio>
              <v-radio label="Online" value="online" style="align-items: flex-start;">
                <div slot="label">
                  <span>Online</span>
                  <v-text-field
                    :autofocus="true"
                    ref="zoomLinkEl"
                    v-show="whereTeach === 'online'"
                    label="Zoom link"
                    v-model="zoomLink"
                    style="width: 500px;"
                  ></v-text-field>
                </div>
              </v-radio>
              <v-radio v-if="classType == 'private'" value="custom">
                <div slot="label">
                  <div>We’ll work it out</div>
                  <div class="caption">We still need your address to show customers where you are.</div>
                </div>
              </v-radio>
              <v-radio value="other" label="TBA">
              </v-radio>
          </v-radio-group>
          <v-textarea
            v-model="locationOther"
            auto-grow
            box
            label="Other"
            hint="Describe your location"
            rows="1"
            :disabled="whereTeach != 'other'"
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
    props: {
        classType: {
            type: String,
            default: 'group'
        }
    },

    data: () => ({
        isLoading: false,
        whereTeach: 'address',
        venues: [],
        locationVenue: null,
        locationOther: null,
        isPremiumCommunity: false,
        zoomLink: null,
    }),

    created: function () {
        if (this.$store.state.teacherGroupClass) {
            this.whereTeach = this.$store.state.teacherGroupClass.whereTeach || 'address'
            this.locationVenue = this.$store.state.teacherGroupClass.locationVenue
            this.locationOther = this.$store.state.teacherGroupClass.locationOther
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity
            this.zoomLink = this.$store.state.teacherGroupClass.zoomLink
        }
        axios.get('/api/venues/').then((res) => {
            console.log(res)
        })
    },

    computed: {
        title() {
            return this.isPremiumCommunity ? 'Where will the community meet?' : 'Where will the lessons be held?';
        },
    },

    methods: {
        saveData() {
            this.$store.commit('setGroupClass', {
                whereTeach: this.whereTeach,
                locationVenue: this.locationVenue,
                locationOther: this.locationOther,
                zoomLink: this.zoomLink,
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
    },
    watch: {
      whereTeach(v) {
        if (v === 'online') setTimeout(() => this.$refs.zoomLinkEl.$refs.input.focus(), 10);
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>