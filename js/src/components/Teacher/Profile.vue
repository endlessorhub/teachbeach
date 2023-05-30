<template>
    <v-layout align-top justify-center row wrap>
        <v-flex xs12 text-xs-center>
            <form>
            <v-card class="card">
                <v-card-title class="headline" primary-title>
                  Profile
                </v-card-title>
                <v-card-text>
                    <v-text-field
                      name="first_name"
                      v-model.trim="first_name"
                      :error-messages="firstNameErrors"
                      :counter="30"
                      label="First Name"
                      required
                      @input="$v.first_name.$touch()"
                      @blur="$v.first_name.$touch()"
                    ></v-text-field>
                    <v-text-field
                      name="last_name"
                      v-model.trim="last_name"
                      :error-messages="lastNameErrors"
                      :counter="30"
                      label="Last Name"
                      required
                      @input="$v.last_name.$touch()"
                      @blur="$v.last_name.$touch()"
                    ></v-text-field>
                    <v-text-field
                      name="email"
                      v-model.trim="email"
                      :error-messages="emailErrors"
                      label="Email Address"
                      required
                      @input="$v.email.$touch()"
                      @blur="$v.email.$touch()"
                    ></v-text-field>
                      <div v-if="showLoginLink" class="v-messages theme--light error--text" style="text-align: left;">Try to <a @click="$emit('openLoginForm')">login</a></div>
                    <v-text-field
                      name="phone"
                      v-model.trim="phone"
                      :error-messages="phoneErrors"
                      label="Phone Number"
                      required
                      @input="$v.phone.$touch()"
                      @blur="$v.phone.$touch()"
                    ></v-text-field>
                    <v-text-field
                      name="password"
                      browser-autocomplete="new-password"
                      v-model="password"
                      :error-messages="passwordErrors"
                      counter
                      type="password"
                      label="Password"
                      required
                      @input="$v.password.$touch()"
                      @blur="$v.password.$touch()"
                    ></v-text-field>

                    <v-radio-group v-model="timezoneSetupMode" row label="Set Timezone">
                      <v-radio label="set from list" value="timezone"></v-radio>
                      <v-radio label="by your location" value="location"></v-radio>
                    </v-radio-group>

                    <div v-if="timezoneSetupMode === 'location'" class="v-input v-text-field v-input--is-label-active v-input--is-dirty theme--light">
                        <div class="v-input__control">
                          <div class="v-input__slot">
                            <div class="v-text-field__slot">
                              <label aria-hidden="true" class="v-label v-label--active theme--light" style="left: 0px; right: auto; position: absolute;">City (for your time zone)</label>
                              <gmap-autocomplete
                                ref="gooaufield"
                                :value="timezonePlace"
                                placeholder="Start typing name of city and choose from list"
                                @place_changed="setPlace"
                                :types="autocompleteTypes"
                                :options="{fields: ['geometry', 'formatted_address']}"
                              >
                              </gmap-autocomplete>
                            </div>
                          </div>
                        </div>
                    </div>

                    <timezone v-else v-model="timezone" />
                    <v-checkbox v-model="adult"
                      required
                      :error-messages="adultErrors"
                      @change="$v.adult.$touch()">
                      <div slot="label">
                        I am 18 years old or older.
                      </div>
                    </v-checkbox>

                    <div style="text-align: left;">
                      By registering, I agree to <a href="https://www.teachbeach.com/blog/?page_id=51" target="_blank">terms</a> and <a href="https://www.teachbeach.com/blog/?page_id=47" target="_blank">privacy agreement</a>.
                        <v-dialog v-model="terms" class="flex xs12 md8 lg6">
                          <v-card>
                            <v-card-title class="headline grey lighten-2" primary-title>
                              Terms
                            </v-card-title>
                            <v-card-text>
                              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="primary"
                                flat
                                @click="terms = false">
                                I accept
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                        <v-dialog v-model="privacy" class="flex xs12 md8 lg6">
                          <v-card>
                            <v-card-title class="headline grey lighten-2" primary-title>
                              Privacy agreement
                            </v-card-title>
                            <v-card-text>
                              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="primary"
                                flat
                                @click="privacy = false">
                                I accept
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                    </div>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                      <v-spacer></v-spacer>
                    <v-btn @click="next">Next</v-btn>
                </v-card-actions>
            </v-card>
            </form>
        </v-flex>
    </v-layout>
</template>

<script>
import _ from 'lodash'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
import Timezone from '@/components/basic/Timezone'

export default {
    mixins: [validationMixin],
    props: [

    ],
    components: {
        Timezone,
    },

    validations: {
        first_name: { required, maxLength: maxLength(30) },
        last_name: { required, maxLength: maxLength(30) },
        email: { required, email },
        phone: { required, maxLength: maxLength(20) },
        password: { required, minLength: minLength(8) },
        adult: {checked (val) {
            return val
        }},
    },

    data: function () {
        return {
            first_name: this.$store.state.user ? this.$store.state.user.first_name : '',
            last_name: this.$store.state.user ? this.$store.state.user.last_name : '',
            email: this.$store.state.user ? this.$store.state.user.email : '',
            phone: this.$store.state.user ? this.$store.state.user.phone : '',
            password: '',
            timezonePlace: '',
            place: null,
            lat: null,
            lng: null,
            adult: false,
            terms: false,
            privacy: false,
            isLoading: false,
            showLoginLink: false,
            is_company: true,
            timezoneSetupMode: 'timezone',
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            errors: {},
        }
    },

    mounted() {
        if(this.alreadyRegistered) {
            this.$router.push('/teachers/start');
        }
    },

    computed: {
        isBelongingToCompany() {
            return !!this.belongsTo;
        },
        belongsTo() {
            return this.$route.query.c;
        },
        autocompleteTypes() {
            return []
        },
        autocompleteHack() {
            return `new-random-${new Date()-0}-${_.uniqueId()}`
        },

        alreadyRegistered: function () {
            return this.$store.state.user && this.$store.state.user.id;
        },

        firstNameErrors () {
            const errors = []
            if (!this.$v.first_name.$dirty) return errors
            !this.$v.first_name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.first_name.required && errors.push('Name is required.')
            return errors
        },
        lastNameErrors () {
            const errors = []
            if (!this.$v.last_name.$dirty) return errors
            !this.$v.last_name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.last_name.required && errors.push('Name is required.')
            return errors
        },
        emailErrors () {
            const errors = []
            if (this.errors.email) {
                return this.errors.email
            }
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.$v.email.required && errors.push('E-mail is required')
            return errors
        },
        phoneErrors () {
            const errors = []
            if (!this.$v.phone.$dirty) return errors
            !this.$v.phone.maxLength && errors.push('Phone must be at most 20 characters long')
            !this.$v.phone.required && errors.push('Phone is required')
            return errors
        },
        adultErrors () {
            //console.log('check adult')
            const errors = []
            if (!this.$v.adult.$dirty) return errors
            !this.$v.adult.checked && errors.push('You must confirm you are over 18 years old to continue!')
            return errors
        },
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters long')
            return errors
        },

    },

    methods: {
        next() {
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            //make axios call
            this.showLoginLink = false
            this.isLoading = true
            let _this = this
            axios.post('/api/users/', {
                first_name: this.first_name,
                last_name: this.last_name,
                email: this.email,
                phone: this.phone,
                password: this.password,
                timezonePlace: this.timezonePlace,
                lat: this.lat,
                lng: this.lng,
                timezone: this.timezone,
                is_company: this.isBelongingToCompany ? false : this.is_company,
                belongs_to: this.belongsTo,
            }).then((res) => {
                //console.log(arguments)

                axios.get('/api/handshake/').then((initial) => {
                    const params = new URLSearchParams();
                    params.append('username', res.data.email)
                    params.append('password', _this.password)
                    params.append('csrftoken', initial.data.csrftoken)
                    axios.post('/api/auth/login/', params).then((loginRes) => {
                        console.log(loginRes)
                        _this.$store.commit('setUser', _.omit(res.data, 'password'))
                        fbq('trackCustom', 'teacherWizard', {step: 'register'})
                        fbq('trackCustom', 'teacherRegistration')
                        this.$router.push('/teachers/start');
                    }).catch(function () {
                        console.log('err!', arguments)
                    }).then(() => {
                        _this.isLoading = false
                    })
                }).catch(function () {
                    //console.log(arguments)
                }).then(() => {

                })
            }).catch((err) => {
                ///handle errors
                _this.isLoading = false
                if (err.response.data) {
                    let errs = {}
                    _.each(err.response.data, (v, k) => {
                        if(k === 'email' && v.indexOf("User with this email already exists") !== -1) {
                            this.showLoginLink = true
                        }
                        errs[k] = v
                    })
                    _this.errors = errs
                }

            })
        },
        clear () {
            this.$v.$reset()
            this.first_name = ''
            this.last_name = ''
            this.email = ''
            this.phone = ''
        }
    },
    watch: {
        place(val) {
            if(val && val.geometry) {
                this.lat = val.geometry.location.lat()
                this.lng = val.geometry.location.lng()
                this.timezonePlace = val.formatted_address
            }
        },
        timezoneSetupMode: {
            handler: function (val) {
                if(val === 'location') {
                    let tmpid = this.autocompleteHack
                    setTimeout(() => {
                        this.$refs.gooaufield.$el.setAttribute('autocomplete', tmpid)
                        this.$refs.gooaufield.$el.autocomplete = tmpid
                    }, 500)
                }
            },
            immediate: true,
        },
        email() {
            if(this.errors.email)
                this.errors.email = undefined
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.card {
    margin: 1em auto;
    width: 480px;
}
</style>