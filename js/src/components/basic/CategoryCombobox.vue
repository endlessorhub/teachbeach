<template>
<v-combobox
  v-model="selectedItems"
  :items="menuItems"
  :label="label"
  :multiple="multiple"
  @change="sendVal"
  chips
  dense
  :menu-props="menuProps"
  :placeholder="placeholder"
  @focus="isMunuOpened=true"
  @blur="isMunuOpened=false"
  :search-input.sync="searchInput"
  browser-autocomplete="new-password"
>
    <template v-slot:selection="{ item, parent, selected }">
      <v-chip
        :selected="selected"
        label
        small
      >
        <span class="pr-2">
          {{ item.text }}
        </span>
        <v-icon
          small
          @click="parent.selectItem(item)"
        >close</v-icon>
      </v-chip>
    </template>
</v-combobox>
</template>

<script>
import _ from 'lodash'

export default {
    props: {
        items: Array,
        label: String,
        id: Number,
        selected: [Array, Object],
        multiple: Boolean,
    },

    data: () => ({
        //select: null
        menuProps: {
            "maxHeight":900,
            //"offset-overflow": true,
            "offset-x": true,
        },
        selectedModel: [],
        isMunuOpened: false,
        searchInput: '',
    }),

    computed: {
        selectedItems: {
            get() {
                return this.selectedModel
            },
            set(val) {
                this.selectedModel = _.concat([], val)
            }
        },
        menuItems() {
            return _.sortBy(this.items, 'text')
        },
        placeholder() {
            return this.isMunuOpened ? 'Type in new category' : ''
        }
    },

    watch: {
        selected(newVal, oldVal) {
            // console.log('selected', newVal, oldVal)
            this.$nextTick(() => {
                this.selectedModel = newVal
            })
        },
        searchInput(newVal, oldVal) {
            console.log(newVal)
            this.$emit('update:input-string', {
                id: this.id,
                value: newVal
            })
        }
    },

    created: function () {

        //this.select = this.selected
    },

    mounted() {
        console.log('combo mounted', this.label, this.selected)
        this.selectedItems = this.selected
    },

    methods: {
        sendVal() {
            this.$emit('update:selection', {
                id: this.id,
                value: this.selectedItems
            })
        },
        onInput(event) {
            console.log(event)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>