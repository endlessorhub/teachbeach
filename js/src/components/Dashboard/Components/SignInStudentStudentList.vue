<template>
    <v-radio-group :value="value" class="full-width" @change="e => $emit('input', e)">
        <v-list
          two-line
        >
          <v-list-tile
                  v-for="item in studentsAvailable"
                  :key="item.id"
                  @click.prevent="isAvailable(item) && $emit('input', item.id)"
                  v-if="isAvailable(item)"
          >
            <v-list-tile-action>
              <v-radio
                :value="item.id"
                :disabled="!isAvailable(item)"
              ></v-radio>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>{{item.first_name}} {{item.last_name}}</v-list-tile-title>
              <v-list-tile-sub-title>Available Lessons: {{item.num_lessons-item.reserved_lessons}}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
    </v-radio-group>
</template>

<script>

export default {
    name: 'dashboard_component_signinstudent_student_list',
    data() {
        return {

        }
    },
    props: [
        'isAvailable',
        'studentsAvailable',
        'value',
    ],
    components: {

    },
    created() {

    },
    computed: {

    },
    methods: {

    },

    watch: {

    }
}
</script>
<style lang="scss" scoped>

</style>