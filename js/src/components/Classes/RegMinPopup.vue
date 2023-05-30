<template>
    <v-dialog
      v-model="value"
      width="400"
      persistent
    >
      <v-card>
        <v-card-title>
            <span class="reg-min-title">{{registrationTitle}}</span>
            <v-spacer></v-spacer>
            <v-btn icon @click="$emit('input', false)">
              <v-icon>close</v-icon>
            </v-btn>
        </v-card-title>
        <v-card-text>
          <RegMinForm v-bind="regMinFormData" v-on:done="v => $emit('done', v)"/>
        </v-card-text>
      </v-card>
    </v-dialog>
</template>

<script>

import RegMinForm from '@/components/basic/forms/RegMin'

export default {
    props: [
        'value',
        'registrationTitle',
        'isPrivate',
        'class_id',
        'alertText',
        'teacherPhone',
    ],
    components: {
        RegMinForm,
    },
    computed: {
        regMinFormData() {
            return {
                'isPrivate': this.isPrivate,
                'class_id': this.class_id,
                'alertText': this.alertText,
                'teacherPhone': this.teacherPhone,
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.reg-min-title {
    width: 85%;
    font-size: 1.4em;
    font-weight: bold;
}
</style>