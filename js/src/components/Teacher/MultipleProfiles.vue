<template>
  <form>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
          <v-flex v-if="teachersList.length > 1" xs12 text-xs-left>
              <v-layout align-top justify-center row wrap>
                  <v-flex sm4 xs12 class="text-sm-left text-xs-center">
                      <v-btn @click="prevTeacher">
                        <v-icon dark left>
                          keyboard_arrow_left
                        </v-icon>
                        Prev Instructor
                      </v-btn>
                  </v-flex>
                  <v-flex sm4 xs12 class="text-xs-center">
                      <v-select
                        v-model="currentTeacher"
                        :items="teachersList"
                        label="Instructor"
                        :menu-props="{maxHeight: 1024}"
                      ></v-select>
                  </v-flex>
                  <v-flex sm4 xs12 class="text-sm-right text-xs-center">
                      <v-btn @click="nextTeacher">
                        Next Instructor
                        <v-icon right dark>
                          keyboard_arrow_right
                        </v-icon>
                      </v-btn>
                  </v-flex>
              </v-layout>
          </v-flex>
          <v-flex xs12 class="text-xs-left">
              <v-btn v-if="editTeacherAvailable" @click="editTeacher">Edit</v-btn>
              <v-btn v-if="addTeacherAvailable" @click="addTeacher">Add another Instructor</v-btn>
          </v-flex>
          <v-flex xs12 text-xs-left>
              <v-text-field
                  :readonly="readonly"
                  v-model.trim="first_name"
                  :error-messages="firstNameErrors"
                  :counter="30"
                  label="First Name"
                  required
                  @input="$v.first_name.$touch();isUpdated=true"
                  @blur="$v.first_name.$touch()"
              ></v-text-field>
              <v-text-field
                  :readonly="readonly"
                  v-model.trim="last_name"
                  :error-messages="lastNameErrors"
                  :counter="30"
                  label="Last Name"
                  required
                  @input="$v.last_name.$touch();isUpdated=true"
                  @blur="$v.last_name.$touch()"
              ></v-text-field>
              <v-text-field
                  :readonly="readonly"
                  v-model.trim="phone"
                  label="Phone (optional)"
                  @input="isUpdated=true"
              ></v-text-field>
              <v-text-field
                  :readonly="readonly"
                  v-model.trim="email"
                  label="Email (optional)"
                  @input="isUpdated=true"
              ></v-text-field>
          </v-flex>
          <v-flex xs12 class="text-xs-left">
              <h4>What makes them special?</h4>
          </v-flex>
        <v-flex xs12 class="text-xs-left">
            <div class="font-weight-medium">Tips: </div>
            <ul class="caption">
                <li>Describe their background, experience years teaching</li>
                <li>Describe approach</li>
                <li>List any relevant accomplishments </li>
            </ul>
        </v-flex>
        <v-flex xs12 text-xs-left>
            <v-textarea
                :readonly="readonly"
                v-model="description"
                auto-grow
                box
                label="What makes them stand out as a instructor?"
                rows="3"
                @input="isUpdated=true"
            ></v-textarea>
        </v-flex>
        <v-flex xs12 class="text-xs-left">

            <ImageUploadCrop
                :readonly="readonly"
                :imageUrl="imageUrl"
                :imageName="imageName"
                :imageFile="imageFile"
                width="400px"
                @change="onFileChanged"
                :aspectRatio="1.25"
            ></ImageUploadCrop>

        </v-flex>
          <v-flex xs12 class="text-xs-left">
              <v-btn v-if="editTeacherAvailable" @click="editTeacher">Edit</v-btn>
              <v-btn v-if="addTeacherAvailable" @click="addTeacher">Add another Instructor</v-btn>
          </v-flex>
      </v-layout>
    </v-container>
      <slot :saveTeacherLocal="saveTeacherLocal">

      </slot>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import { validationMixin } from 'vuelidate'
import { required, maxLength} from 'vuelidate/lib/validators'

import ImageUploadCrop from '@/components/basic/ImageUploadCrop'

export default {
    mixins: [validationMixin],
    validations: {
        first_name: { required, maxLength: maxLength(30) },
        last_name: { required, maxLength: maxLength(30) },
    },
    components: {
        ImageUploadCrop
    },
    props: {
        teachers: {
            type: Array,
            default: [],
        },
        selectedTeacher: {
            type: Number,
            default: null,
        },
        reloadTeachers: {
            type: Function,
        },
        saveTeacher: {
            type: Function,
        },
    },

    data: function () { return {
        isLoading: false,
        isUpdated: false,
        crop: {},
        readonly: true,
        ignoreChange: false,
        currentTeacher: this.selectedTeacher,

        imageName: '',
        imageUrl: '',
		imageFile: '',
        teachers: [],
        first_name: '',
        last_name: '',
        phone: '',
    }},

    created: function () {
        this.readonly = !!this.currentTeacher
    },

    computed: {
        editTeacherAvailable() {
            return !!this.teachers.length
        },
        addTeacherAvailable() {
            return !!this.teachers.length
        },
        teacherObj() {
            return {
                first_name: this.first_name,
                last_name: this.last_name,
                phone: this.phone,
                email: this.email,
                description: this.description,
                id: this.currentTeacher,
            }
        },
        teachersList() {
            return _.map(this.teachers, t => ({
                text: `${t.first_name || ''} ${t.last_name || ''}`,
                value: t.id,
            }))
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

    },

    methods: {
        editTeacher() {
            this.readonly = false
        },
        addTeacher() {
            if(!this.currentTeacher) {
                this.saveTeacherLocal();
                this.saveTeacher().then((res) => {
                    if(res && res.data && res.data.id) {
                        this.isUpdated = false
                        this.currentTeacher = res.data.id
                        this.setTeacher(null)
                        this.reloadTeachers()
                    }
                }).catch((e) => {
                    console.log('err!', e)
                })
            } else
                this.currentTeacher = null
        },
        prevTeacher() {
            const ids = _.map(this.teachers, 'id')
            let index = _.findIndex(ids, id => this.currentTeacher === id)
            this.currentTeacher = index === -1 || !(--index in ids) ? ids[ids.length-1] : ids[index]
        },
        nextTeacher() {
            const ids = _.map(this.teachers, 'id')
            let index = _.findIndex(ids, id => this.currentTeacher === id)
            this.currentTeacher = index === -1 || !(++index in ids) ? ids[0] : ids[index]
        },
        onFileChanged(e) {
            if(this.ignoreChange) {
                this.ignoreChange = false
                return
            }
            this.isUpdated = true
            this.imageName = e.imageName
            this.imageFile = e.imageFile
            this.imageUrl = e.imageUrl
            this.crop = e.crop
        },
        setTeacher(id) {
            const newTeacher = _.find(this.teachers, {id: id})
            this.first_name = newTeacher ? newTeacher.first_name : ''
            this.last_name = newTeacher ? newTeacher.last_name : ''
            this.phone = newTeacher ? newTeacher.phone : ''
            this.email = newTeacher ? newTeacher.email : ''
            this.description = newTeacher ? newTeacher.description : ''
            //this.ignoreChange = newTeacher && newTeacher.media ? true : false
            this.imageUrl = newTeacher ? newTeacher.media : ''
            this.imageName = ''
            this.imageFile = ''
            this.currentTeacher = id
            //this.isUpdated = false
        },
        saveTeacherLocal(profileParams = {}) {
            this.$v.$touch()
            if (this.$v.$anyError)
                return Promise.resolve(false)
            this.$store.commit('setTeacherProfile', _.assign({
                description: this.description,
                first_name: this.first_name,
                last_name: this.last_name,
                phone: this.phone,
                email: this.email,
                id: this.currentTeacher,
            }, profileParams))
            this.$store.commit('setTeacher', _.assign({
                description: this.description,
                first_name: this.first_name,
                last_name: this.last_name,
                phone: this.phone,
                email: this.email,
                id: this.currentTeacher,
            }, profileParams))
            this.$store.commit('setTeacherAvatar', {
                uploadPhoto: {
                    imageName: this.imageName,
                    imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                    imageFile: this.imageFile,
                },
            })
        }
    },
    watch: {
        currentTeacher(newId, oldId) {
            this.readonly = !!newId
            if(this.isUpdated) {
                this.saveTeacherLocal({id: oldId});
                this.saveTeacher().then((res) => {
                    if(res) {
                        this.reloadTeachers().then(res => {
                            this.setTeacher(newId)
                        })
                    }
                }).catch((e) => {
                    console.log('err!', e)
                })
            } else {
                this.setTeacher(newId)
            }
        },
        teachers() {
            if(this.currentTeacher)
                this.setTeacher(this.currentTeacher)
        },
        isUpdated(newVal, oldVal) {
            console.log('isUpdated', oldVal, '->', newVal)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>