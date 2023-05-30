<template>
    <v-dialog v-if="item" v-model="value" max-width="700px" persistent>
        <v-card>
          <v-card-title>
            <span class="headline">Invite student to "{{item.name}}"</span>
          </v-card-title>

          <v-card-text>

              <v-layout wrap>
                <v-flex xs12 text-xs-left>
                    <span class="title">Click send to send an online payment form to your student.</span>
                </v-flex>
                <v-flex xs12>
                  <form>
                      <v-radio-group v-model="addStudentFormType" mandatory row>
                          <v-radio label="New Student" value="new"></v-radio>
                          <v-radio label="Existing" value="registered"></v-radio>
                      </v-radio-group>
                    <v-text-field
                      name="name"
                      v-if="addStudentFormType === 'new'"
                      v-model.trim="addStudentFormName"
                      :error-messages="addStudentFormNameErrors"
                      label="Name"
                      required
                      @input="$v.addStudentFormName.$touch()"
                      @blur="$v.addStudentFormName.$touch()"
                    ></v-text-field>
                    <v-text-field
                      v-if="addStudentFormType === 'new'"
                      name="email"
                      v-model.trim="addStudentFormEmail"
                      :error-messages="addStudentFormEmailErrors"
                      label="Email Address"
                      required
                      @input="$v.addStudentFormEmail.$touch()"
                      @blur="$v.addStudentFormEmail.$touch()"
                    ></v-text-field>
                      <v-autocomplete
                          v-else
                          v-model="addStudentFormAutocompleteEmail"
                          :items="students"
                          chips
                          hide-no-data
                          label="Type in a name or email"
                          :filter="emailAutocompleteFilter"
                          :error-messages="addStudentFormAutocompleteEmailErrors"
                          @input="$v.addStudentFormAutocompleteEmail.$touch()"
                          @blur="$v.addStudentFormAutocompleteEmail.$touch()"
                      >
                        <template v-slot:selection="data">
                            <v-chip
                              :selected="false"
                              class="chip--select-multi"
                              outline
                            >
                              <v-avatar>
                                <v-icon dark>account_circle</v-icon>
                              </v-avatar>
                                <span style="color: black;">{{ data.item.first_name }} {{ data.item.last_name }} <b> ({{data.item.email}})</b></span>
                            </v-chip>
                        </template>
                        <template v-slot:item="data">
                            <template v-if="typeof data.item !== 'object'">
                              <v-list-tile-content v-text="data.item"></v-list-tile-content>
                            </template>
                            <template v-else>
                              <v-list-tile-avatar>
                                <v-avatar>
                                    <v-icon dark>account_circle</v-icon>
                                </v-avatar>
                              </v-list-tile-avatar>
                              <v-list-tile-content>
                                <v-list-tile-title>{{data.item.first_name}} {{data.item.last_name}}</v-list-tile-title>
                                <v-list-tile-sub-title v-html="data.item.email"></v-list-tile-sub-title>
                              </v-list-tile-content>
                            </template>
                        </template>
                      </v-autocomplete>
                    <v-text-field
                      v-if="addStudentFormType === 'new'"
                      name="phone"
                      v-model.trim="addStudentFormPhone"
                      :error-messages="addStudentFormPhoneErrors"
                      label="Phone Number"
                    ></v-text-field>
                    <v-checkbox
                        v-model="addStudentFormCopyMe"
                        label="Send me a copy"
                    ></v-checkbox>
                    <v-textarea
                        v-model="addStudentFormMessage"
                        auto-grow
                        box
                        label="Add message"
                        rows="3"
                    ></v-textarea>
                  </form>
                    <v-alert
                      :value="addStudentFormError"
                      color="info"
                    >
                        {{addStudentFormError}}
                    </v-alert>
                </v-flex>
              </v-layout>

          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="close()">Cancel</v-btn>
            <v-btn color="primary" @click="addStudentFormConfirm">Send</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
import axios from 'axios'
import ActionableOnClick from '@/components/basic/ActionableOnClick'
import { mapMutations } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, requiredIf, email } from 'vuelidate/lib/validators'

export default {
    name: 'dashboard_teach_add_student_dialog',
    mixins: [validationMixin],
    components: {

    },
    data: () => ({
        addStudentFormType: 'new',
        addStudentFormName: '',
        addStudentFormPhone: '',
        addStudentFormEmail: '',
        addStudentFormMessage: '',
        addStudentFormError: '',
        addStudentFormAutocompleteEmail: null,
        addStudentFormCopyMe: false,
    }),
    props: [
        'value',
        'item',
        'students',
    ],
    validations: {
        addStudentFormAutocompleteEmail: {required: requiredIf(function (model) {return this.addStudentFormType !== 'new'})},
        addStudentFormEmail: {required: requiredIf(function (model) {return this.addStudentFormType === 'new'}), email},
        addStudentFormName: {required: requiredIf(function (model) {return this.addStudentFormType === 'new'})},
    },
    computed: {
        addStudentFormNameErrors() {
            const errors = []
            if (!this.$v.addStudentFormName.$dirty) return errors
            !this.$v.addStudentFormName.required && errors.push('Name is required')
            return errors
        },
        addStudentFormPhoneErrors() {
            return []
        },
        addStudentFormEmailErrors() {
            const errors = []
            if (!this.$v.addStudentFormEmail.$dirty) return errors
            !this.$v.addStudentFormEmail.email && errors.push('Must be valid e-mail')
            !this.$v.addStudentFormEmail.required && errors.push('E-mail is required')
            return errors
        },
        addStudentFormAutocompleteEmailErrors() {
            const errors = []
            if (!this.$v.addStudentFormAutocompleteEmail.$dirty) return errors
            !this.$v.addStudentFormAutocompleteEmail.required && errors.push('Find the existing student first')
            return errors
        }
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        close() {
            this.$emit('input', false);
        },
        emailAutocompleteFilter(item, text) {
            return text.split(' ').some(text => text && (item.email.includes(text) || item.first_name.includes(text) || item.last_name.includes(text)))
        },
        addStudentFormConfirm() {
            if(this.$v.$anyError)
                return
            axios.post(`/api/send_add_student_request/`, {
                class_id: this.item.id,
                name: this.addStudentFormType === 'new' ? this.addStudentFormName : '',
                email: this.addStudentFormType === 'new' ? this.addStudentFormEmail : this.addStudentFormAutocompleteEmail.email,
                phone: this.addStudentFormType === 'new' ? this.addStudentFormPhone : '',
                message: this.addStudentFormMessage,
                type: this.addStudentFormType,
                copyMe: this.addStudentFormCopyMe,
            }).then(res => {
                if(res.data.success)
                    this.close()
                else {
                    this.setGlobalError(res.data.error_message)
                }
            }).catch(e => console.error(e)).then(() => {
                this.isLoading = false
            })
        },
        companyName(item) {
            return item.teacher.user.is_company && item.teacher.user.company_profile ? `
${item.teacher.user.company_profile.name}` : '';
        },
    },
    watch: {
        item(val, old) {
            if(val && val.id && (!old || old.id !== val.id)) {
                this.addStudentFormMessage = `You’re invited to "${this.item.name}".
Book here: ${window.location.origin}/learners/${this.item.id}/3/?name=&phone=&email=

All the best,
${this.item.teacher.first_name} ${this.item.teacher.last_name}${this.companyName(this.item)}
${this.item.teacher.phone || this.item.teacher.user.phone}
${this.item.teacher.email || this.item.teacher.user.email}

Powered by TeachBeach.com`
            }
        }
    }
}
</script>
<style lang="scss" scoped>

</style>