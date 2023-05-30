<template>
      <v-card>
        <v-card-text v-if="isMessageSent">
            <div class="text-xs-center">
                <v-badge
                  color="platform-green"
                  left
                  overlap
                >
                      <template v-slot:badge>
                        <v-icon
                          dark
                          small
                        >
                          done
                        </v-icon>
                      </template>
                    <v-avatar
                      v-if="avatar"
                      :size="100"
                      color="grey lighten-4"
                    >
                      <img :src="avatar" alt="avatar">
                    </v-avatar>
                </v-badge>
            </div>
            <div class="text-xs-center">
                <div class="headline mb-0">Message sent. Great job!</div>
            </div>
            <div>
                Excited to start your learning journey?<br/>
                Book lesson now and secure the best lesson time.
            </div>
            <div>
                <v-btn
                    v-if="showBookBtn"
                    :loading="isLoading"
                    :disabled="isLoading"
                    class="platform-green"
                    @click="bookLesson"
                >
                    Book lesson
                </v-btn>
            </div>
        </v-card-text>
        <v-card-text v-else>
            <div class="text-xs-center">
                <v-avatar
                  v-if="avatar"
                  :size="100"
                  color="grey lighten-4"
                >
                  <img :src="avatar" alt="avatar">
                </v-avatar>
            </div>
            <div class="text-xs-center">
                <div class="headline mb-0">Contact {{contact.first_name}}</div>
            </div>
          <v-textarea
              v-model.trim="message"
              outline
              :label="`Hey ${contact.first_name}!`"
              :error-messages="messageErrors"
              required
              placeholder="Write your message here"
              @input="$v.message.$touch()"
              @blur="$v.message.$touch()"
          ></v-textarea>
            <div v-if="phone">Or call <a :href="`tel:${phone}`">{{phone}}</a></div>
            <v-checkbox
                v-if="includeAllowOther"
                v-model="allowOther"
                label="Allow other suitable tutors to contact me ">
            </v-checkbox>
            <div class="text-xs-center">
              <v-btn
                :loading="isLoading"
                :disabled="isLoading"
                class="platform-green"
                @click="submitMessage"
              >
                Send message
              </v-btn>
            </div>
        </v-card-text>

        <v-card-actions>

        </v-card-actions>
      </v-card>
</template>
<script>
import _ from 'lodash'
import axios from 'axios'
import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'

import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'

export default {
    name: 'form_send_message',
    mixins: [validationMixin],
    data: () => ({
        isLoading: false,
        message: '',
        allowOther: false,
        checkErrors: false,
        isMessageSent: false,
    }),
    props: [
        'contact',
        'avatar',
        'additional',
        'showBookBtn',
        'phone',
        'includeAllowOther',
    ],
    validations: {
        message: { required },
    },
    components: {

    },
    created() {

    },
    computed: {
        messageErrors() {
            const errors = []
            if(!this.checkErrors)
                return errors
            if (!this.$v.message.$dirty) return errors
            !this.$v.message.required && errors.push('Message is required.')
            return errors
        },
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        submitMessage() {
            this.checkErrors = true
            this.$v.$touch()
            //console.log('submit', this, arguments)
            if (this.$v.message.$anyError)
                return
            this.isLoading = true
            axios.post(`/api/message/`, {
                message: this.message,
                to: _.pick(this.contact, ['entity', 'id']),
                allowOther: this.allowOther,
                additional: this.additional,
            }).then(res => {
                if(!res.data.status) {
                    this.setGlobalError(res.data.err);
                    return new Error(res.data.err)
                }
                this.$emit('done', res.data)
                this.message = ''
                this.isMessageSent = true
            }).catch(e => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
                this.checkErrors = false
            })
        },
        bookLesson() {
            this.$emit('bookLesson')
        }
    },

    watch: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>