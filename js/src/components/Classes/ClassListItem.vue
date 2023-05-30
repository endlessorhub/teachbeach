<template>
  <v-card class="class-list-item">
      <v-img
          v-if="avatar"
          :src="avatar"
          aspect-ratio="2"
      ></v-img>
      <v-card-title primary-title>
      <div>
          <h3 class="headline mb-0"><router-link :to="'/class/'+id">{{title}}</router-link></h3>
        <h4> {{ isPrivate ? "Private" : "Group" }} </h4>
      </div>
    </v-card-title>
    <v-card-text>
        <v-btn v-if="can_enroll" class="platform-green" :to="'/learners/new_enroll/'+id+'/4/0'">Enroll</v-btn>
        <div v-if="location" class="class-list-item__location"><v-icon>location_on</v-icon>{{location}}</div>
        <div class="class-list-item__description">{{description}}</div>
    </v-card-text>
  </v-card>
</template>

<script>
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    props: {
        id: {
            type: Number,
            default: 0,
        },
        title: {
            type: String,
            default: '',
        },
        isMasterClass: {
            type: Boolean,
            default: false,
        },
        isEditorPick: {
            type: Boolean,
            default: false,
        },
        isPrivate: {
            type: Boolean,
            default: false,
        },
        freqDates: {
            type: String,
            default: '',
        },
        location: {
            type: String,
            default: '',
        },
        teacher: {
            type: String,
            default: '',
        },
        price: {
            type: String,
            default: '',
        },
        from: {
            type: String,
            default: '',
        },
        to: {
            type: String,
            default: '',
        },
        avatar: {
            type: String,
            default: '',
        },
        description: {
            type: String,
            default: '',
        },
        can_enroll: {
            type: Boolean,
            default: true,
        },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.class-list-item {
    width: 300px;
    height: 500px;
    overflow: hidden;
    &__description {
        overflow: hidden;
    }
}
</style>