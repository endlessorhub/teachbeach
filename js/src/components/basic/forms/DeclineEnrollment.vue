<template>
    <v-dialog
      v-model="opened"
      max-width="390"
    >
      <v-card>
        <v-card-title class="headline">
            Add a reason
          <v-spacer></v-spacer>
          <v-btn icon @click.native="opened = false" color="gray darken-1">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-text-field
              v-model.trim="declineReason"
              label="Decline reason"
              :error-messages="declineReasonErrors"
              required
              @input="$v.declineReason.$touch()"
              @blur="$v.declineReason.$touch()"
          ></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-btn
            :disabled="isLoading"
            flat="flat"
            @click="opened = false"
          >
            Decide later
          </v-btn>
          <v-spacer></v-spacer>

          <v-btn
            :loading="isLoading"
            :disabled="isLoading"
            class="platform-green"
            flat="flat"
            @click="submitDecline"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</template>
<script>
import _ from 'lodash'
import axios from 'axios'
import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'

import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
    name: 'form_decline_enrollment',
    mixins: [validationMixin],
    data: () => ({
        isLoading: false,
        declineReason: '',
        opened: false,
    }),
    props: [
        'enrollment',
    ],
    validations: {
        declineReason: { required },
    },
    components: {

    },
    created() {

    },
    computed: {
        declineReasonErrors() {
            const errors = []
            if (!this.$v.declineReason.$dirty) return errors
            !this.$v.declineReason.required && errors.push('Reason is required.')
            return errors
        },
    },
    methods: {
        open() {
            this.declineReason = ''
            this.opened = true
        },
        rejectEnroll(id) {
            this.currentDeclineEnrollmentId = id
            this.opened = true
            this.declineReason = ''
        },
        submitDecline() {
            this.$v.$touch()
            //console.log('submit', this, arguments)
            if (this.$v.declineReason.$anyError)
                return
            this.isLoading = true
            axios.post(`/api/private_enroll/${this.enrollment.id}/reject/`, {reason: this.declineReason}).then(res => {
                this.declineReason = ''
                this.opened = false
                this.isLoading = false
                this.$emit('done')
            })
        },
    },

    watch: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>