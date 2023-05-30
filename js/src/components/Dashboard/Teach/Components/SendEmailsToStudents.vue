<template>
    <div class="text-xs-center">
        <slot name="activator" :click="onActivatorClick">
            <v-btn @click="onActivatorClick">Send Emails</v-btn>
        </slot>
        <v-dialog v-model="sendEmailsForm" persistent max-width="500px">
            <bulk-email-send-form
                :student-filter="studentFilter"
                @cancel="sendEmailsForm = false"
                ref="bulkEmailForm"
            />
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios'
import BulkEmailSendForm from './BulkEmailSendForm'

export default {
    name: 'send_emails_to_students',
    components: {
        BulkEmailSendForm,
    },
    data: () => ({
        sendEmailsForm: false,
        sendEmailsFormError: '',
        sendEmailsFormLoading: false,
        sendEmailsFormSent: false,
        sendEmailsFormText: '',
    }),
    props: {
        'studentFilter': {
            type: String,
            default: 'students',
        }
    },
    computed: {

    },
    methods: {
        sendEmailsFormSubmit() {
            if(this.sendEmailsFormSent) {
                return this.sendEmailsFormClose()
            }
            this.sendEmailsFormLoading = true
            axios.post('/api/teacher_students_email/', {text: this.sendEmailsFormText, filter: this.studentFilter}).then(res => {
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
            this.sendEmailsForm = false
            this.$refs.bulkEmailForm.cleanUp()
        },
        onActivatorClick() {
            this.sendEmailsForm=true
        }
    },
    watch: {
        sendEmailsForm(v) {
            if(!v)
                this.$refs.bulkEmailForm.cleanUp()
        }
    },
}
</script>
<style lang="scss">

</style>