<template>
    <li :key="key">
        <div class="image hidden-sm-and-down">
            <Image300
                v-if="avatar"
                height="110"
                width="137"
                :src="avatar"
            >
            </Image300>
        </div>
        <div class="text">
            <div class="title">
                <router-link :to="'/class/'+id">{{ title }}</router-link>
                <v-chip v-if="isMasterClass" label class="small-chip">MASTER CLASS</v-chip>
                <v-chip v-if="isEditorPick" label class="small-chip">EDITOR PICK</v-chip>
            </div>
            <div class="description">
                <div>{{ description }}</div>
                <div>
                  <b v-if="venue">{{venue}}</b>
                    {{ location }}
                  <span class="padded">{{ price }}</span>
                  <span class="padded">{{ schedule }}</span>
                </div>
            </div>
            <div><router-link :to="`/class/${id}`">Read more</router-link></div>
        </div>
        <div class="cta">
            <v-btn v-if="isEnrollable" class="platform-green" @click.stop.prevent="bookClass()" style="width: 90%;">
                {{isTrialAvailable ? 'Book a '+(trialPackageRate ? `$${trialPackageRate}` : 'free')+' trial' : 'See package rates'}}
            </v-btn>
            <v-btn v-if="classItem.is_private" @click.stop.prevent="openMessageForm()" style="width: 90%;">
                Send message
            </v-btn>
            <div v-if="!isPrivate">{{from}}</div>
            <div v-if="!isPrivate">{{to}}</div>
        </div>
        <v-dialog
          v-model="contactDialog"
          persistent
          width="400"
          lazy
        >
          <v-card>
            <v-card-title>
                <v-spacer></v-spacer>
                <v-btn icon @click="closeSendMessage">
                  <v-icon>close</v-icon>
                </v-btn>
            </v-card-title>
            <v-card-text>
              <SendMessageForm v-if="sendMessageFormData && sendMessageFormData.contact" v-bind="sendMessageFormData" v-on:done="messageDone" v-on:bookLesson="bookClass"/>
            </v-card-text>
          </v-card>
        </v-dialog>

        <v-dialog
          v-model="registerDialog"
          width="400"
          persistent
          lazy
        >
          <v-card>
            <v-card-title>
                {{registrationTitle}}
                <v-spacer></v-spacer>
                <v-btn icon @click="registerDialog = false">
                  <v-icon>close</v-icon>
                </v-btn>
            </v-card-title>
            <v-card-text>
              <RegMinForm v-bind="regMinFormData" v-on:done="registerDone"/>
            </v-card-text>
          </v-card>
        </v-dialog>
    </li>
</template>

<script>

import SendMessageForm from '@/components/basic/forms/SendMessage'
import RegMinForm from '@/components/basic/forms/RegMin'
import Image300 from '@/components/basic/Image300'
import classItemMixin from '@/mixins/classItem'

export default {
    props: [
        'id',
        'key',
        'classItem',
        'title',
        'isMasterClass',
        'isEditorPick',
        'isPrivate',
        'isEnrollable',
        'instantAvailable',
        'freqDates',
        'location',
        'teacher',
        'price',
        'from',
        'to',
        'schedule',
        'avatar',
        'description',
        'venue',
    ],
    data: () => ({
        contactDialog: false,
        sendMessageFormData: {
            includeAllowOther: false,
        },
        registerDialog: false,
        initAction: '',
        registrationTitle: '',
    }),
    components: {
        SendMessageForm,
        RegMinForm,
        Image300,
    },
    mixins: [
        classItemMixin,
    ],
    computed: {
        currentClass() {
            return this.classItem;
        },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>