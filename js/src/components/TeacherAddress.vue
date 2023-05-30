<template>
  <form autocomplete="off">
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <input autocomplete="false" name="hidden" type="text" style="display:none;">
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 md6 class="text-xs-left" order-xs2 order-md1>
          <GmapMap
            @click="onClickMap"
            :center="center"
            :zoom="zoom"
            map-type-id="terrain"
            :style="computedStyle"
          >
            <GmapMarker
              v-if="lat && lng"
              label=""
              :position="markerPosition"
            ></GmapMarker>
          </GmapMap>
        </v-flex>
        <v-flex xs12 md6 class="text-xs-left" order-xs1 order-md2>
          <v-combobox
              v-if="isCompany"
              v-model="teachingVenue"
              label="Name of venue"
              :items="venuesList"
              @change="updateLoc"
              :error-messages="teachingVenueErrors"
              required
              @input="$v.teachingVenue.$touch()"
              @blur="$v.teachingVenue.$touch()"
              :browser-autocomplete="autocompleteHack"
              ref="venueCombobox"
          >
          </v-combobox>
          <div class="v-input v-text-field v-input--is-label-active v-input--is-dirty theme--light">
            <div class="v-input__control">
              <div class="v-input__slot">
                <div class="v-text-field__slot">
                  <label aria-hidden="true" class="v-label v-label--active theme--light" style="left: 0px; right: auto; position: absolute;">{{autocompleteLabel}}</label>
                  <gmap-autocomplete
                    ref="gooaufield"
                    :value="teachingGooglePlace"
                    placeholder="Start typing or click on map"
                    @place_changed="setPlace"
                    :types="autocompleteTypes"
                    :options="{fields: ['geometry', 'formatted_address', 'address_components']}"
                  >
                  </gmap-autocomplete>
                </div>
              </div>
            </div>
          </div>
          <v-text-field
            v-model="teachingCountry"
            label="Country"
            readonly
            :disabled="isFieldDisabled('teachingCountry')"
          ></v-text-field>
          <v-text-field
            v-model="teachingState"
            label="State"
            readonly
            :disabled="isFieldDisabled('teachingState')"
          ></v-text-field>
          <v-text-field
            v-model="teachingAddress"
            label="Address"
            :error-messages="teachingAddressErrors"
            required
            @input="$v.teachingAddress.$touch()"
            @blur="$v.teachingAddress.$touch()"
            readonly
            :disabled="isFieldDisabled('teachingAddress')"
          ></v-text-field>
          <v-text-field
            v-model="teachingStreet"
            label="Street"
            readonly
            :disabled="isFieldDisabled('teachingStreet')"
          ></v-text-field>
          <v-combobox
            v-model="teachingCity"
            :items="citiesList"
            label="City"
            prepend-icon="location_searching"
            readonly
            :disabled="isFieldDisabled('teachingCity')"
          >
          </v-combobox>
          <v-text-field
            v-model="teachingZip"
            label="ZIP"
            readonly
            :disabled="isFieldDisabled('teachingZip')"
          ></v-text-field>
        </v-flex>
        <v-flex v-if="errorMessage" xs12 class="text-xs-left" order-xs3>
            <v-alert type="error" :value="true" color="platform-error">
              {{errorMessage}}
            </v-alert>
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
import {gmapApi} from 'vue2-google-maps'

import { validationMixin } from 'vuelidate'
import { required, maxLength, requiredIf, sameAs, minLength } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],

    validations: {
        teachingAddress: { required: requiredIf('isNotTBA') },
        teachingVenue: { required: requiredIf('isCompany') },
    },

    props: [
        'isCompany'
    ],

    data: () => ({
        isLoading: false,
        teachingVenue: '',
        teachingCountry: '',
        teachingState: '',
        teachingAddress: '',
        teachingStreet: '',
        teachingCity: '',
        teachingZip: '',
        teachingGooglePlace: '',
        citiesList: [],
        place: null,
        zoom: 15,
        lat: null,
        lng: null,
        geocoder: null,
        errorMessage: '',
        venues: [],
        isEditable: true,
        whereTeach: 'address',
    }),

    created: function () {
        let _this = this
        if (this.$store.state.teacherGroupClass) {
            this.whereTeach = _this.$store.state.teacherGroupClass.whereTeach
            this.teachingCountry = _this.$store.state.teacherGroupClass.teachingCountry
            this.teachingState = _this.$store.state.teacherGroupClass.teachingState
            this.teachingAddress = _this.$store.state.teacherGroupClass.teachingAddress
            this.teachingStreet = _this.$store.state.teacherGroupClass.teachingStreet
            this.teachingCity = _this.$store.state.teacherGroupClass.teachingCity
            this.teachingZip = _this.$store.state.teacherGroupClass.teachingZip
            this.teachingGooglePlace = _this.$store.state.teacherGroupClass.teachingGooglePlace
            this.lat = _this.$store.state.teacherGroupClass.lat
            this.lng = _this.$store.state.teacherGroupClass.lng
        }
        this.isLoading = true
        axios.all([axios.get('/api/cities/'), axios.get('/api/company_venues/')]).then(axios.spread((cities, venues) => {
            this.citiesList = _.map(cities.data, (v) => ({
                text: v,
                value: v,
            }))
            this.venues = venues.data
            if (this.venues.length) {
                this.teachingVenue = _this.$store.state.teacherGroupClass.teachingVenue
            } else if (this.isCompany) {
                this.teachingVenue = this.$store.state.teacherGroupClass.teachingVenue || this.$store.state.companyProfile.companyName
            }
            // this.teachingVenue = _this.$store.state.teacherGroupClass.teachingVenue || this.$store.state.teacherGroupClass.compa
        })).catch(() => {

        }).then(() => {
            this.isLoading = false
        })
    },

    mounted() {
        this.$nextTick(() => {
            let tmpid = this.autocompleteHack
            setTimeout(() => {
                this.$refs.gooaufield.$el.setAttribute('autocomplete', tmpid)
                this.$refs.gooaufield.$el.autocomplete = tmpid
            }, 500)
		});
    },

    computed: {
        isNotTBA() {
            return this.whereTeach !== 'other'
        },
        autocompleteTypes() {
            return this.whereTeach === 'other' ? ['(regions)'] : []
        },
        autocompleteLabel() {
            return this.whereTeach === 'other' ? 'City name or ZIP code' : 'Street address'
        },
        autocompleteHack() {
            return `new-random-${new Date()-0}-${_.uniqueId()}`
        },
        venuesList() {
            return _.map(this.venues, (v) => v.teaching_venue)
        },
        google: gmapApi,
        markerPosition() {
            return {
                lat: this.lat,
                lng: this.lng,
            }
        },
        computedStyle() {
            return {
                width: '100%',
                height: '300px',
            }
        },
        center() {
            if(this.lat && this.lng) {
                return {lat:this.lat, lng:this.lng}
            }
            return {lat:27.7676008, lng:-82.6402915}
        },
        teachingAddressErrors () {
            const errors = []
            if (!this.$v.teachingAddress.$dirty) return errors
            if (this.whereTeach === 'other') return errors
            !this.$v.teachingAddress.required && errors.push('Address is required.')
            return errors
        },
        teachingVenueErrors() {
            const errors = []
            if (!this.$v.teachingVenue.$dirty) return errors
            !this.$v.teachingVenue.required && errors.push('Venue name is required.')
            return errors
        }
    },

    methods: {
        updateLoc() {
            console.log('update venue')
            let found = _.find(this.venues, {teaching_venue: this.teachingVenue})
            let existingVenue = _.find(this.venues, {lat: this.lat, lng: this.lng})
            if(found) {
                this.teachingCountry = found.address_country
                this.teachingState = found.address_state
                this.teachingAddress = found.address
                this.teachingStreet = found.address_street
                this.teachingCity = found.address_city
                this.teachingZip = found.address_zip
                this.teachingGooglePlace = found.teachingGooglePlace
                this.lat = found.lat
                this.lng = found.lng
            } else if (existingVenue) {
                this.teachingCountry = ''
                this.teachingState = ''
                this.teachingAddress = ''
                this.teachingStreet = ''
                this.teachingCity = ''
                this.teachingZip = ''
                this.teachingGooglePlace = ''
                this.lat = null
                this.lng = null
            }
        },
        onClickMap(event) {
            console.log('onClickMap', arguments)
            this.lat = event.latLng.lat()
            this.lng = event.latLng.lng()
            if(!this.geocoder) {
                this.geocoder = new google.maps.Geocoder
            }
            this.geocoder.geocode({'location': {lat: this.lat, lng: this.lng}}, (results, status) => {
                if (status === 'OK') {
                    if (results[0]) {
                        this.setPlace(results[0])
                        /*
                        console.log(results, status)
                        let tmpVar
                        this.teachingCountry = (tmpVar = _.find(results[0].address_components, v => v.types.indexOf("country") > -1)) ? tmpVar.long_name : ''
                        this.teachingState = (tmpVar = _.find(results[0].address_components, v => v.types.indexOf("administrative_area_level_1") > -1)) ? tmpVar.short_name : ''
                        this.teachingCity = (tmpVar = _.find(results[0].address_components, v => v.types.indexOf("locality") > -1)) ? tmpVar.long_name : ''
                        this.teachingAddress = (tmpVar = _.find(results[0].address_components, v => v.types.indexOf("street_number") > -1)) ? tmpVar.long_name : ''
                        this.teachingStreet = (tmpVar = _.find(results[0].address_components, v => v.types.indexOf("route") > -1)) ? tmpVar.long_name : ''
                        this.teachingZip = (tmpVar = _.find(results[0].address_components, v => v.types.indexOf("postal_code") > -1)) ? tmpVar.long_name : ''
                        this.teachingVenue = ''
                        */
                    } else {
                        console.log('no result', results, status)
                    }
                } else {
                    console.log('fail', results, status)
                }
            });
        },
        setPlace(place) {
            this.place = place
        },
        saveData() {
            this.$store.commit('setGroupClass', {
                teachingVenue: this.teachingVenue,
                teachingCountry: this.teachingCountry,
                teachingState: this.teachingState,
                teachingAddress: this.teachingAddress,
                teachingStreet: this.teachingStreet,
                teachingCity: this.teachingCity && this.teachingCity.value ? this.teachingCity.value : this.teachingCity,
                teachingZip: this.teachingZip,
                teachingGooglePlace: this.teachingGooglePlace,
                lat: this.lat,
                lng: this.lng,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            this.$nextTick(() => {
                // hacky fix of venue input without commit (by select or blur)
                setTimeout(() => {
                    console.log(this.place)
                    if (!this.lat || !this.lng || !this.teachingCity) {
                        this.errorMessage = 'Place point on map or find your location typing text into street address field'
                        return
                    }
                    this.$v.$touch()
                    if (this.$v.$anyError)
                        return
                    this.saveData()
                    this.$emit('next:step')
                }, 100)
            })
        },
        clear () {

        },
        isFieldDisabled(fieldName) {
            if(this.whereTeach === 'other')
                return true
            return false
        },
    },
    watch: {
        place(val) {
            if(val) {
                this.lat = val.geometry.location.lat()
                this.lng = val.geometry.location.lng()
                //place.address_components
                let tmpVar
                this.teachingCountry = (tmpVar = _.find(val.address_components, v => v.types.indexOf("country") > -1)) ? tmpVar.long_name : ''
                this.teachingState = (tmpVar = _.find(val.address_components, v => v.types.indexOf("administrative_area_level_1") > -1)) ? tmpVar.short_name : ''
                this.teachingCity = (tmpVar = _.find(val.address_components, v => v.types.indexOf("locality") > -1)) ? tmpVar.long_name : ''
                // accordingly https://developers.google.com/places/supported_types
                if(!this.teachingCity)
                    this.teachingCity = (tmpVar = _.find(val.address_components, v => v.types.indexOf("administrative_area_level_3") > -1)) ? tmpVar.long_name : ''
                // not always city available
                if(!this.teachingCity)
                    this.teachingCity = (tmpVar = _.find(val.address_components, v => v.types.indexOf("postal_town") > -1)) ? tmpVar.long_name : ''
                this.teachingAddress = (tmpVar = _.find(val.address_components, v => v.types.indexOf("street_number") > -1) || val.address_components[0]) ? tmpVar.long_name : ''
                this.teachingStreet = (tmpVar = _.find(val.address_components, v => v.types.indexOf("route") > -1)) ? tmpVar.long_name : ''
                this.teachingZip = (tmpVar = _.find(val.address_components, v => v.types.indexOf("postal_code") > -1)) ? tmpVar.long_name : ''
                this.teachingGooglePlace = val.formatted_address
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>