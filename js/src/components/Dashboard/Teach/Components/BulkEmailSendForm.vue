<template>
    <v-card>
      <v-card-title>
        Send Emails
      </v-card-title>

      <v-card-text>
        <v-checkbox
          v-model="sendEmailsCopyMe"
          label="Copy me on this message"
        ></v-checkbox>
        <v-text-field
          label="Subject"
          hide-details
          v-model="sendEmailsFormSubject"
        ></v-text-field>
        <v-input
          name="email_text"
          outline
          light
          placeholder="Add text that will be sent to all students in the list"
          auto-grow
        ></v-input>
        <wysiwyg
          class="text-container"
          v-model="sendEmailsFormText"
        ></wysiwyg>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn v-if="!sendEmailsFormSent" color="primary" flat @click="sendEmailsFormClose">Cancel</v-btn>
        <v-btn :loading="sendEmailsFormLoading" :disabled="sendEmailsFormLoading" :color="sendEmailsFormSent ? 'platform-green' : 'primary'" @click="sendEmailsFormSubmit">{{sendEmailsFormSent ? 'Done' : 'Send'}}</v-btn>
      </v-card-actions>
    </v-card>
</template>
<script>
import axios from 'axios'

const initialhtml = '';

export default {
    name: 'bulk_email_send_form',
    data: () => ({
        sendEmailsFormError: '',
        sendEmailsFormLoading: false,
        sendEmailsFormSent: false,
        sendEmailsFormText: initialhtml,
        sendEmailsFormSubject: '',
        sendEmailsCopyMe: true,
    }),
    props: {
        'studentFilter': {
            type: String,
            default: 'students',
        },
        'studentList': {
            type: String,
            default: () => {[]},
        }
    },
    computed: {

    },
    methods: {
        sendEmailsFormSubmit() {
            if(!this.sendEmailsFormText)
                return;
            if(this.sendEmailsFormSent) {
                return this.sendEmailsFormClose()
            }
            this.sendEmailsFormLoading = true
            axios.post('/api/teacher_students_email/', {
                subject: this.sendEmailsFormSubject,
                text: this.sendEmailsFormText,
                filter: this.studentFilter,
                students: this.studentList,
                copyMe: this.sendEmailsCopyMe,
            }).then(res => {
                if(res.data.success) {
                    this.sendEmailsFormSent = true
                } else {
                    this.sendEmailsFormError = res.data.error
                }
            }).catch(e => console.log(e)).then(() => {
                this.sendEmailsFormLoading = false
            })
        },
        sendEmailsFormClose() {
            this.cleanUp()
            this.$emit('cancel')
        },
        cleanUp() {
            if(this.sendEmailsFormSent)
                this.sendEmailsFormText = initialhtml;
            this.sendEmailsFormSent = false;
        }
    },
    watch: {

    },
}
</script>
<style lang="scss" scoped>
.text-container {
  text-align: left;
}
</style>