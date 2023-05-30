<template>
  <div class="home">
    <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-center waves-container" :style="waveStyle">
            <SearchboxHome
                style="margin-top: 100px;"
            ></SearchboxHome>
        </v-flex>
        <v-flex xs12 class="text-xs-left" v-if="!screenXS">
            <!--v-img :src="meetTheTeachers" width="265"></v-img-->
            <h2 class="padded" style="margin: 0;">Ready to jump in?</h2>
        </v-flex>

        <v-flex xs12 class="text-xs-center teachers-block" v-if="!screenXS">
            <v-layout align-start justify-center row wrap>
                <v-flex v-for="(val, i) in classesFormatted" md4 sm6 xs12 text-xs-center class="class-card" :key="val.id">
                    <div class="title text-xs-left font-weight-bold">{{val.category}}</div>
                    <router-link :to="`/class/${val.id}`" style="text-decoration: none; color: black;">
                        <v-img v-if="val.imageUrl" :src="val.imageUrl" aspect-ratio="1.25"></v-img>
                    </router-link>
                    <div class="class-name">
                        <router-link :to="`/class/${val.id}`" style="text-decoration: none; color: black;">{{val.name}}</router-link>
                    </div>
                    <v-layout align-left justify-center row nowrap>
                        <v-flex xs3 class="text-xs-center teacher-avatar">
                            <v-avatar v-if="val.avatarUrl">
                              <img
                                :src="val.avatarUrl"
                                :alt="val.teacherName"
                              >
                            </v-avatar>
                        </v-flex>
                        <v-flex xs9 class="text-xs-left teachers-info">
                            <div class="teacher-name">
                                <router-link :to="`/teacher_profile/${val.teacherId}`" style="text-decoration: none; color: black;">{{val.teacherName}}</router-link>
                            </div>
                            <div class="company-name">{{val.companyName}}</div>
                        </v-flex>
                    </v-layout>
                </v-flex>
            </v-layout>
        </v-flex>

        <v-flex xs12 class="text-xs-center three-buttons-block">
            <v-layout align-center justify-center row wrap>
                <v-flex sm4 xs12 class="text-xs-center">
                    <v-btn flat class="three-button-btn" @click="searchClassesAll">See All Classes</v-btn>
                </v-flex>
                <v-flex sm4 xs12 class="text-xs-center">
                    <v-btn flat class="three-button-btn" @click="requestAClassOpen">Request A Class</v-btn>
                </v-flex>
                <v-flex sm4 xs12 class="text-xs-center">
                    <v-btn flat class="three-button-btn" to="/teachers/light-register">Become An Instructor</v-btn>
                </v-flex>
            </v-layout>
        </v-flex>

        <v-flex xs12 class="text-xs-left" v-if="!screenXS">
            <v-img :src="aboutUs" width="139"></v-img>
            <!--h2 class="padded">About Us</h2-->
        </v-flex>

        <v-flex xs12 class="text-xs-center about-us-block" v-if="!screenXS">
            <v-layout align-start justify-center row wrap>
                <v-flex v-for="(val, i) in aboutUsBlocks" md3 sm6 xs12 text-xs-center class="about-us-card" :key="i">
                    <div class="about-us-card__title">{{val.title}}</div>
                    <div class="about-us-card__text">{{val.text}}</div>
                </v-flex>
            </v-layout>
        </v-flex>

        <v-flex xs12 class="text-xs-left get-on-container">
            <div>
                <v-img :src="getOnTheList" width="208"></v-img>
                <!--h2 style="color: white;">Get On The List!</h2-->
            </div>
            <div>
                Sign up to see new classes, and exclusive offerings.
            </div>
            <v-layout align-top justify-center row wrap>
                <v-flex md3 xs6 class="text-xs-center hor-padded">
                    <v-text-field
                      background-color="white"
                      v-model.trim="email"
                      :error-messages="emailErrors"
                      placeholder="Email"
                      @input="$v.email.$touch()"
                      @blur="$v.email.$touch()"
                      aria-label="Email"
                    ></v-text-field>
                </v-flex>
                <v-flex md3 xs6 class="text-xs-center hor-padded">
                    <v-text-field
                      background-color="white"
                      v-model.trim="cityText"
                      placeholder="City"
                      aria-label="City"
                    ></v-text-field>
                </v-flex>
                <v-flex md3 xs6 class="text-xs-center hor-padded">
                    <div class="inline">
                        <div>
                            <v-checkbox
                              color="white"
                              dark
                              height="20"
                              hide-details
                              v-model="iamLearner"
                              label="I'm a learner"
                            ></v-checkbox>
                        </div>
                        <div>
                            <v-checkbox
                              color="white"
                              dark
                              height="20"
                              hide-details
                              v-model="iamTeacher"
                              label="I am a teacher"
                            ></v-checkbox>
                        </div>
                    </div>
                </v-flex>
                <v-flex md3 xs6 class="text-xs-center hor-padded" style="padding-top: 8px;">
                    <v-btn flat class="three-button-btn" @click="signUpNow">Sign Up Now</v-btn>
                    <v-dialog
                      v-model="signUpDialog"
                      max-width="290"
                    >
                      <v-card>
                        <v-card-title class="headline">Thank you</v-card-title>

                        <v-card-text>
                          Your request has been sent
                        </v-card-text>

                        <v-card-actions>
                          <v-spacer></v-spacer>

                          <v-btn
                            color="green darken-1"
                            flat="flat"
                            @click="signUpDialog = false"
                          >
                            Ok
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                </v-flex>
            </v-layout>
        </v-flex>

        <v-flex xs12 class="text-xs-center footer-block">
            <v-layout align-start justify-center row wrap>
                <v-flex v-for="(val, i) in footerBlocks" md4 sm6 xs12 text-xs-center class="footer-card" :key="i">
                    <div class="footer-card__title">{{val.title}}</div>
                    <div v-for="(item, j) in val.items" class="footer-card__item" :key="j">
                        <router-link v-if="item.url && item.isLocal" :to="item.url">{{item.name}}</router-link>
                        <a v-else-if="item.url" :href="item.url">{{item.name}}</a>
                        <span v-else>{{item.name}}</span>
                    </div>
                </v-flex>
            </v-layout>
        </v-flex>
    </v-layout>
    <v-dialog v-model="requestAClassDialog" width="400">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>
            <div>Request a class</div>
            <v-spacer></v-spacer>
            <v-btn icon dark @click="requestAClassDialog = false">
              <v-icon>close</v-icon>
            </v-btn>
        </v-card-title>
        <v-card-text>
            <div>We’ll find your teacher! What would you like to learn?</div>
            <v-flex xs12 text-xs-center>
                <v-text-field
                  name="requestAClassTopic"
                  v-model.trim="requestAClassTopic"
                  :error-messages="requestAClassTopicErrors"
                  label="Topic"
                  required
                  @input="$v.requestAClassTopic.$touch()"
                  @blur="$v.requestAClassTopic.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 text-xs-center>
                <v-text-field
                  name="requestAClassEmail"
                  v-model.trim="requestAClassEmail"
                  :error-messages="requestAClassEmailErrors"
                  label="Email"
                  required
                  @input="$v.requestAClassEmail.$touch()"
                  @blur="$v.requestAClassEmail.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 text-xs-center>
                <v-text-field
                  name="requestAClassPhone"
                  v-model.trim="requestAClassPhone"
                  :error-messages="requestAClassPhoneErrors"
                  label="Phone"
                  required
                  @input="$v.requestAClassPhone.$touch()"
                  @blur="$v.requestAClassPhone.$touch()"
                ></v-text-field>
            </v-flex>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="requestAClassSend" :disabled="isLoading">
            Send request
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import wavesPng from '@/assets/waves.png'
import meetTheTeachers from '@/assets/meet_the_teachers.png'
import aboutUs from '@/assets/about_us.png'
import getOnTheList from '@/assets/get_on_the_list.png'
import transparentImg from '@/assets/transparent.png'
import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import metadata from '@/mixins/metadata'
import SearchboxHome from '@/components/basic/SearchboxHome'
import classHelper from '@/lib/helpers/Class'
import { mapMutations } from 'vuex'

export default {
    mixins: [validationMixin, metadata],
    validations: {
        email: { required, email },
        requestAClassEmail: { required, email },
        requestAClassPhone: { required },
        requestAClassTopic: { required },
    },
    name: 'home',
    components: {
        SearchboxHome,
    },
    data: () => ({
        isLoading: false,
        classesLoaded: [],
        carouselInit: false,
        curSlide: 0,
        hackySlide: {},
        zip: null,
        citiesList: [],
        zipsList: [],
        waveStyle: {
            backgroundImage: `url('${wavesPng}')`,
            height: '295px',
            backgroundRepeat: 'repeat-x',
            marginTop: '20px',
            backgroundSize: 'contain',
        },
        meetTheTeachers,
        aboutUs,
        getOnTheList,
        signUpDialog: false,
        email: '',
        cityTextUpdated: '',
        iamLearner: false,
        iamTeacher: false,
        aboutUsBlocks: [
            {
                title: 'Certified',
                text: 'We curate the best live local classes and private instructors.',
            },
            {
                title: 'Unique',
                text: 'We invite local experts with unique skills.',
            },
            {
                title: 'Simple',
                text: 'Find a teacher, book and pay online.',
            },
            {
                title: 'Guaranteed',
                text: 'We guarantee your experience.',
            },
        ],
        footerBlocks: [
            {
                title: 'Company',
                items: [
                    {name: 'About us', url: 'https://www.teachbeach.com/blog/?page_id=11'},
                    {name: 'Blog', url: 'https://www.teachbeach.com/blog/'},
                ],
            },
            {
                title: 'Information',
                items: [
                    {name: 'Privacy policy', url: 'https://www.teachbeach.com/blog/?page_id=47'},
                    {name: 'Terms', url: 'https://www.teachbeach.com/blog/?page_id=51'},
                    {name: 'Help for teachers', url: 'https://www.teachbeach.com/blog/?page_id=2'},
                    {name: 'Help for students', url: 'https://www.teachbeach.com/blog/?page_id=42'},
                ],
            },
            {
                title: 'Contact us',
                items: [
                    {name: 'Become an instructor', url: '/teachers/light-register', isLocal: true},
                    {name: 'Alisa@teachbeach.com', url: 'mailto:alisa@teachbeach.com'},
                    {name: '408.892.9815', url: 'tel:4088929815'},
                ],
            },
        ],
        requestAClassDialog: false,
        requestAClassPhone: '',
        requestAClassEmail: '',
        requestAClassTopic: '',
    }),
    props: [
        'city',
        'category',
        'subcategory',
    ],
    created() {
        if(this.city) {
            this.updateClasses(this.city)
        } else {
            this.updateClasses({
                address_city: 'online',
                address_state: 'none'
            })
        }
    },
    mounted: function () {

    },
    computed: {
        screenXS() {
            return this.$vuetify.breakpoint.xsOnly
        },
        cityText: {
            get() {
                if(this.cityTextUpdated) {
                    return this.cityTextUpdated
                }
                /*
                if(this.city && this.city.address_city && this.city.address_state) {
                    return `${this.city.address_city}, ${this.city.address_state}`
                }
                */
                return ''
            },
            set(v) {
                this.cityTextUpdated = v
            }

        },
        emailErrors() {
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            return errors
        },
        requestAClassEmailErrors() {
            const errors = []
            if (!this.$v.requestAClassEmail.$dirty) return errors
            !this.$v.requestAClassEmail.required && errors.push('Email is required.')
            !this.$v.requestAClassEmail.email && errors.push('Must be valid e-mail')
            return errors
        },
        requestAClassPhoneErrors () {
            const errors = []
            if (!this.$v.requestAClassPhone.$dirty) return errors
            !this.$v.requestAClassPhone.required && errors.push('Phone is required.')
            return errors
        },
        requestAClassTopicErrors () {
            const errors = []
            if (!this.$v.requestAClassTopic.$dirty) return errors
            !this.$v.requestAClassTopic.required && errors.push('Topic is required.')
            return errors
        },
        showBlock() {
            return this.city ? 'carousel' : 'image'
        },
        carouselOptions() {
            return {
                perPage: 3,
                loop: false,
            }
        },
        classesFormatted() {
            let res = _.map(this.classesLoaded, (c) => {
                return {
                    imageUrl: classHelper.previewImageSrc(c.master_media) || transparentImg,
                    name: c.is_private ? c.private_className : c.name,
                    id: c.id,
                    avatarUrl: classHelper.previewImageSrc(c.teacher.media),
                    teacherName: `${c.teacher.first_name} ${c.teacher.last_name}`,
                    companyName: c.teacher.user.is_company ? c.teacher.user.company_profile.name : '',
                    teacherId: c.teacher.id,
                    category: c.category,
                }
            })
            return res
        },
        carouselPrev() {
            return this.curSlide
        },
        carouselNext() {
            return this.curSlide+3 < this.classesFormatted.length
        },
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        requestAClassOpen() {
            this.requestAClassTopic = ''
            this.requestAClassEmail = ''
            this.requestAClassPhone = ''
            this.requestAClassDialog = true
        },
        requestAClassSend() {
            this.$v.$touch()
            if(this.requestAClassEmail.$anyError || this.requestAClassTopic.$anyError || this.requestAClassPhone.$anyError)
                return
            this.isLoading = true
            axios.post('/api/request_class', {
                email: this.requestAClassEmail,
                phone: this.requestAClassPhone,
                topic: this.requestAClassTopic,
            }).then(res => {
                if(!res.data.status) {
                    this.setGlobalError(res.data.err);
                    return new Error(res.data.err)
                }
                this.requestAClassDialog = false
            }).catch(e => {
                console.log(e)
            }).then(res => {
                this.isLoading = false
            })
        },
        signUpNow() {
            this.$v.$touch()
            if(this.email.$anyError)
                return
            this.isLoading = true
            axios.post('/api/newsletter', {
                email: this.email,
                city: this.cityText,
                is_learner: this.iamLearner,
                is_teacher: this.iamTeacher,
            }).then(res => {
                this.signUpDialog = true
            }).catch(e => {
                console.log(e)
            }).then(res => {
                this.isLoading = false
            })
        },
        updateClasses(city) {
            this.isLoading = true
            axios.post('/api/most_recent_classes/', {
                category: null,
                city: city.address_city,
                state: city.address_state,
                subcategory: null,
            }).then(res => {
                this.isLoading = false
                this.classesLoaded = _.filter(res.data, v => v.master_media)
            })
        },
        changeCarouselFunc() {
            //console.log(arguments)
        },
        searchClasses(category=undefined, subcategory=undefined) {
            if(this.city == 'online') {
                this.$router.push(`/learners/search/online/none/${category || this.category || '0'}/${typeof subcategory === 'undefined' ? this.subcategory || '' : subcategory}`)
            } else {
                if(this.city)
                    this.$router.push(`/learners/search/${this.city.address_city}/${this.city.address_state}/${category || this.category || '0'}/${typeof subcategory === 'undefined' ? this.subcategory || '' : subcategory}`)
                else {
                    this.$router.push(`/learners/search/all/all/${category || this.category || '0'}/${typeof subcategory === 'undefined' ? this.subcategory || '' : subcategory}`)
                }
            }
        },
        searchClassesAll() {
            return this.searchClasses('0', '')
        },
        searchClassesCustom() {
            this.searchClasses()
        }
    },

    watch: {
        city(newCity, oldCity) {
            //this.$store.commit('setCity', newCity)
            this.$store.commit('setLearnerSearch', {city: newCity})
            if(newCity) {
                this.updateClasses(newCity)
            }
        },
        zip(newZip) {
            //this.$store.commit('setZip', newZip)
            this.$store.commit('setLearnerSearch', {zip: newZip})
        },

    }
}
</script>
<style lang="scss">
.parent-of-switched {
    position: relative;
}
.default-image, .overlay-button-block {
    position: absolute;
    right: 0;
    left: 0;
}
.carousel-container {
    position: absolute;
    top: 120px;
    right: 0;
    left: 0;
    //height: 300px;
}
.v-carousel {
  width: 100%;
  position: relative;
  overflow: hidden;
  //box-shadow: 0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12);

  &__prev,
  &__next {
    position: absolute;
    top: 50%;
    z-index: 1;
    transform: translateY(-50%);

    .v-btn {
      margin: 0;
      height: auto;
      width: auto;

      i {
        font-size: 48px;
      }

      &:hover {
        background: none;
      }
    }
  }

  &__prev {
    left: 5px;
  }
  &__next {
    right: 5px;
  }
}

.home {
    h1 {
        font-size: 2.6rem;
    }
    h2 {
        font-size: 2rem;
    }
    .waves-container {
        border-bottom: solid 10px #95d807;
        margin-bottom: 80px
    }
    .teachers-block {
        margin-bottom: 80px
    }
    .class-card {
        padding: 20px;

        .class-name {
            text-align: left;
            font-size: 1.5em;
        }
        .teacher-name {

        }
        .company-name {
            color: gray;
        }
    }
    .three-buttons-block {
        border-bottom: solid 10px #95d807;
        background-color: #00bfd9;
        margin-bottom: 80px;
    }
    .three-button-btn {
        background-color: white;
        width: 200px;
        text-transform: none;
    }
    .about-us-block {
        margin-top: 10px;
        margin-bottom: 80px;

        .about-us-card {
            padding: 0 20px;
            font-size: 1.2em;
            border-right: 1px solid #00bfd9;

            &__title {
                font-weight: bold;
            }
            &__text {

            }
            &:last-child {
                border-right: none;
            }
        }

    }
    .footer-block {
        margin-bottom: 40px;

        .footer-card {
            padding: 0 20px;
            font-size: 1.2em;

            &__title {
                font-weight: bold;
            }
            &__item {
                a {
                    text-decoration: none;
                    color: black;
                }
            }

        }

    }
    .get-on-container {
        border-bottom: solid 10px #95d807;
        margin-bottom: 40px;
        background-color: #00bfd9;
        padding: 10px;
        color: white;

        .hor-padded {
            padding: 0 5px;
        }
        .inline > div {
            display: inline-block;
            width: 50%;
        }
    }
    .h-padded {
        padding: 0 10px;
    }
}
</style>