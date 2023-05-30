<template>
    <v-radio-group :value="value" hide-details @change="v => $emit('change', v)">
        <template v-slot:append>
            <v-tooltip top content-class="teachbeach-tooltip">
                <template v-slot:activator="{ on }">
                  <v-icon v-on="on">help_outline</v-icon>
                </template>
                <span>Busy teaching? Don’t miss calls!<br/>
                    Registration adds all prospects to your CRM.<br/>
                    “Text only” option allows you to respond <br/>
                    as soon as  you are free.
                </span>
            </v-tooltip>
        </template>
      <v-radio
        label="Registered customers can  text and see phone number"
        value="call"
      ></v-radio>
      <v-radio
        label="Registered customers can text only"
        value="text"
      ></v-radio>
    </v-radio-group>
</template>
<script>
export default {
    model: {
        prop: 'value',
        event: 'change'
    },
    props: {
        value: {
            type: String,
            default: 'text',
        },
    },
}
</script>
