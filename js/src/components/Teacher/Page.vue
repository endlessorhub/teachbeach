<template>
  <div class="teachers">
    <div class="teacher-form-container flex xs12">
        <v-stepper v-model="step" alt-labels style="box-shadow: none;">
            <v-stepper-header style="display: none;">
              <v-stepper-step step="1"></v-stepper-step>
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">
              <slot></slot>
              </v-stepper-content>
            </v-stepper-items>
        </v-stepper>
    </div>
  </div>
</template>

<script>
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    name: 'teachers-page',
}
</script>
<style scoped lang="scss">
.teachers {
    text-align: center;
    .teacher-form-container {
        //width: 800px;
        margin: 0 auto;
    }
}
</style>