<template>
    <v-dialog class="base-confirm-action" v-model="isOpened" :width="width">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>
          {{ title }}
        </v-card-title>
        <v-card-text>
          <slot></slot>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            flat
            @click="onCancelClick">
            {{ cancel }}
          </v-btn>
          <v-btn
            color="primary"
            flat
            @click="onConfirmClick" :disabled="isLoading">
            {{ confirm }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>

export default {
    name: 'BaseConfirmAction',
    props: {
        isOpened: {
            type: Boolean,
            default: false,
        },
        isLoading: {
            type: Boolean,
            default: false,
        },
        width: {
            type: Number,
            default: 400,
        },
        title: {
            type: String,
            default: 'Please confirm',
        },
        cancel: {
            type: String,
            default: 'Cancel',
        },
        confirm: {
            type: String,
            default: 'Confirm',
        },
    },
    methods: {
        onCancelClick() {
            this.$emit('cancel');
        },
        onConfirmClick() {
            this.$emit('confirm');
        },
    },
}
</script>
<style lang="scss" scoped>

.base-confirm-action {

}
</style>