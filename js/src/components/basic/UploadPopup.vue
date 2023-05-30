<template>
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on }">
        <slot :loading="isLoading" :on="on" name="popup-open-btn"></slot>
      </template>

      <v-card>
        <v-card-title
          primary-title
        >
          {{popupTitle}}
        </v-card-title>
        <v-card-text v-if="isDone">
            <div>The list was loaded successfully</div>
            <div><b>Added</b>: {{added}}</div>
            <div><b>Skipped</b>: {{skipped}}</div>
        </v-card-text>
        <v-card-text v-else>
            <div class="description">{{popupDescription}}</div>
            <v-text-field
                label="Select File"
                @click='pickFile'
                v-model='fileName'
                prepend-icon='attach_file'
                :loading="isLoading"
                :disabled="isLoading"
            ></v-text-field>
            <input
                type="file"
                style="display: none"
                ref="file"
                :accept="accept"
                @change="onFilePicked"
            >
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            :color="isDone ? 'platform-green' : 'default'"
            @click="dialog = false"
          >
            {{isDone ? 'Done' : 'Cancel'}}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios';
import {mapMutations} from 'vuex';

export default {
    props: {
        url: {
            type: String,
            default: '',
        },
        formatRequest: {
            type: Function,
            default: ({name, url, data}) => ({
                name,
                url,
                data,
            }),
        },
        popupTitle: {
            type: String,
            default: 'Upload a file',
        },
        popupDescription: {
            type: String,
            default: 'Upload a file',
        },
        accept: {
            type: String,
            default: '*/*',
        }
    },

    data: () => ({
        isLoading: false,
        isDone: false,
        fileData: null,
        fileName: null,
        fileUrl: null,
        dialog: false,
        added: 0,
        skipped: 0,
    }),

    created() {

    },

    watch: {
        dialog(newVal) {
            if(newVal)
                this.isDone = false;
        }
    },

    computed: {

    },

    methods: {
        ...mapMutations(['setGlobalError']),
        pickFile() {
            this.$refs.file.click();
        },

        onFilePicked(e) {
            const files = e.target.files;
            if (files[0] !== undefined) {
                this.fileName = files[0].name;
                if (this.fileName.lastIndexOf('.') <= 0) {
                    return;
                }
                const fr = new FileReader();
                fr.readAsDataURL(files[0]);
                fr.addEventListener('load', () => {
                    this.fileUrl = fr.result;
                    this.fileData = files[0];
                    this.upload();
                })
            } else {
                this.fileName = '';
                this.fileData = '';
                this.fileUrl = '';
            }
        },

        upload() {
            this.isLoading = true
            return axios.post(this.url, this.formatRequest({
                name: this.fileName,
                url: this.fileUrl,
                data: this.fileData,
            })).then(res => {
                if(res.data.success) {
                    this.fileName = '';
                    this.fileData = '';
                    this.fileUrl = '';
                    this.isDone = true;
                    this.added = res.data.added
                    this.skipped = res.data.skipped
                    this.$emit('uploaded');
                } else {
                    this.setGlobalError(res.data.error_message)
                }
            }).catch(e => {
                console.log(e);
            }).finally(() => {
                this.isLoading = false
            })
        }
    }
}
</script>

<style lang="scss">
.description {
    text-align: left;
}
</style>