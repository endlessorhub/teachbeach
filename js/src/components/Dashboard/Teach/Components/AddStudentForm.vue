<template>
      <v-layout wrap>
        <v-flex xs12>
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
                  label="Email (or name)"
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
              label="Copy me on this message"
            ></v-checkbox>
            <v-textarea
                v-model="addStudentFormMessage"
                auto-grow
                box
                label="Add message"
                rows="3"
            ></v-textarea>
        </v-flex>
      </v-layout>
</template>
<script>
import { validationMixin } from 'vuelidate'
import { required, requiredIf, email } from 'vuelidate/lib/validators'

const formFeilds = {
    addStudentFormType: 'new',
    addStudentFormName: '',
    addStudentFormPhone: '',
    addStudentFormEmail: '',
    addStudentFormMessage: '',
    addStudentFormAutocompleteEmail: null,
    addStudentFormCopyMe: true,
}

export default {
    name: 'dashboard_teach_add_student_form',
    mixins: [validationMixin],
    components: {

    },
    data() {
        return {
            ...formFeilds,
            addStudentFormError: '',
            //isValid: false,
        }
    },
    props: {
        'value': {
            type: Object,
            default: () => ({
                ...formFeilds
            }),
        },
        'item': {
            type: Object,
            default: {},
        },
        'students': {
            type: Array,
            default: [],
        },
    },
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
        },
        output() {
            return {
                ...Object.keys(formFeilds).reduce((acc, v) => ({...acc, [v]: this[v]}), {}),
                addStudentFormError: this.addStudentFormError,
                isValid: !this.$v.$anyError
            }
        }
    },
    methods: {
        emitUpdate() {
            this.$emit('input', this.output)
        },
        emailAutocompleteFilter(item, text) {
            return text.split(' ').some(text => text && (item.email.includes(text) || item.first_name.includes(text) || item.last_name.includes(text)))
        },
        companyName(item) {
            return item.teacher.user.is_company && item.teacher.user.company_profile ? `
${item.teacher.user.company_profile.name}` : '';
        },
    },
    watch: {
        value: {
            handler(val) {
                for (let k in formFeilds) {
                    if(k in val)
                        this[k] = val[k]
                }
            },
            immediate: true,
            deep: true,
        },
        item: {
            handler: function (val, old) {
                if (val && val.id && (!old || old.id !== val.id)) {
                    this.addStudentFormMessage = `You’re invited to "${this.item.name}".
Book here: ${window.location.origin}/learners/${this.item.id}/3/?name=&phone=&email=

All the best,
${this.item.teacher.first_name} ${this.item.teacher.last_name}${this.companyName(this.item)}
${this.item.teacher.phone || this.item.teacher.user.phone}
${this.item.teacher.email || this.item.teacher.user.email}

Powered by TeachBeach.com`
                }
            },
            immediate: true,
        },
        output(val) {
            this.emitUpdate()
        }
    }
}
</script>
<style lang="scss" scoped>

</style>