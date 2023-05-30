<template>
    <span class="action-list">
        <v-tooltip top v-if="item.isEnrollStudentsAvailable" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon @click="showEnrollStudentsForm(item)" v-on="on"><v-icon>account_circle</v-icon></v-btn>
          </template>
          <span>Sign in students to class "{{item.name}}"</span>
        </v-tooltip>
        <v-tooltip top v-if="!item.isDeactivated && !item.isExpired" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon @click="showAddStudentForm(item)" v-on="on"><v-icon>add</v-icon></v-btn>
          </template>
          <span>Add student to class "{{item.name}}"</span>
        </v-tooltip>
        <v-tooltip top v-if="item.editEnabled" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon :to="'/teachers/class/'+item.id" v-on="on"><v-icon>edit</v-icon></v-btn>
          </template>
          <span>Edit</span>
        </v-tooltip>
        <v-tooltip top v-if="item.deleteEnabled" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon @click="deleteClass(item.id)" v-on="on"><v-icon>delete_outline</v-icon></v-btn>
          </template>
          <span>Delete</span>
        </v-tooltip>
        <v-tooltip top v-if="item.isExpired" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon :to="'/teachers/copy_class/'+item.id" v-on="on"><v-icon>replay</v-icon></v-btn>
          </template>
          <span>Post again</span>
        </v-tooltip>
        <v-tooltip top v-if="item.isDeactivated" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon @click="resumeClass(item.id)" v-on="on" :loading="item.isLoadidngActivation" :disabled="item.isLoadidngActivation">
                <v-icon>play_circle_outline</v-icon>
            </v-btn>
          </template>
          <span>Resume</span>
        </v-tooltip>
        <v-tooltip top v-else content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon @click="pauseClass(item.id)" v-on="on" :loading="item.isLoadidngActivation" :disabled="item.isLoadidngActivation">
                <v-icon>pause_circle_outline</v-icon>
            </v-btn>
          </template>
          <span>Set on Pause</span>
        </v-tooltip>
        <v-tooltip top v-if="!item.isMessageAvailable" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn icon @click="openSendMessageForm(item.id)" v-on="on"><v-icon>message</v-icon></v-btn>
          </template>
          <span>Text this class</span>
        </v-tooltip>
        <v-tooltip top v-if="item.isBoostAvailable" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn
                @click="openBoostForm(item.id)"
                v-on="on"
                icon
            >
                <v-icon color="platform-green">fas fa-rocket</v-icon>
            </v-btn>
          </template>
          <span>Boost this class</span>
        </v-tooltip>
        <v-tooltip top v-else-if="item.isBoosted" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn
                @click="openBoostForm(item.id)"
                v-on="on"
                icon
            >
                <v-icon color="grey">fas fa-rocket</v-icon>
            </v-btn>
          </template>
          <span>Launched!</span>
        </v-tooltip>
        <v-tooltip top v-if="item.isEmailAvailable" content-class="teachbeach-tooltip">
          <template v-slot:activator="{ on }">
            <v-btn
                icon
                @click="openEmailBoostForm(item.id)"
                v-on="on"
            ><v-icon color="platform-green">email</v-icon></v-btn>
          </template>
          <span>Email Boost</span>
        </v-tooltip>
        <v-btn
                v-else-if="item.isEmailBoosted"
                icon
                disabled
        >
            <v-icon color="gray">email</v-icon>
        </v-btn>
    </span>
</template>
<script>
import axios from 'axios'

export default {
    name: 'class_list_item_actions',
    data: () => ({

    }),
    props: [
        'item',
        'showAddStudentForm',
        'showEnrollStudentsForm',
        'deleteClass',
        'resumeClass',
        'openEmailBoostForm',
        'openBoostForm',
        'openSendMessageForm',
        'pauseClass',
    ],
    computed: {

    },
    methods: {

    },
}
</script>
<style lang="scss">
.action-list >>> .v-btn.v-btn--icon {
    margin: -6px -2px;
}
</style>