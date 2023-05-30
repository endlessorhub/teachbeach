<template>
  <form>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
            <div>Customers are 3x more likely to hire when they see a photo.</div>
            <v-flex xs12 class="text-xs-center text-sm-center text-md-center text-lg-center">
                <ImageUploadCrop
                    :imageUrl="imageUrl"
                    :imageName="imageName"
                    :imageFile="imageFile"
                    width="400px"
                    @change="onFileChanged"
                    :aspectRatio="1.25"
                ></ImageUploadCrop>
            </v-flex>
            <div>Sure, you can use a logo, but photos have a higher response.</div>
        </v-flex>

      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import axios from 'axios'

export default {
    components: {
        ImageUploadCrop
    },

    data: () => ({
        isLoading: false,
        imageName: '',
        imageUrl: '',
		imageFile: '',
        crop: {},
    }),

    created: function () {
        let _this = this
        if (this.$store.state.avatar && this.$store.state.avatar.uploadPhoto) {
            this.imageName = _this.$store.state.avatar.uploadPhoto.imageName || ''
            this.imageUrl = _this.$store.state.avatar.uploadPhoto.imageUrl || ''
            this.imageFile = _this.$store.state.avatar.uploadPhoto.imageFile || ''
        }
    },

    computed: {

    },

    methods: {
        saveData() {
            this.$store.commit('setTeacherAvatar', {
                uploadPhoto: {
                    imageName: this.imageName,
                    imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                    imageFile: this.imageFile,
                },
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        onFileChanged(e) {
            this.isUpdated = true
            this.imageName = e.imageName
            this.imageFile = e.imageFile
            this.imageUrl = e.imageUrl
            this.crop = e.crop
        },
        submit () {
            this.saveData()
            //make axios call
            this.isLoading = true
            axios.post('/api/teacher_profile/', {
                profile: this.$store.state.profile,
                avatar: this.$store.state.avatar,
            }).then((res) => {
                console.log('/api/teacher_profile/', arguments)
                this.$store.commit('setTeacherProfile', {id: res.data.id})
                this.$store.commit('setTeacher', {id: res.data.id})
                this.$emit('next:step')
            }).catch(() => {
                console.log('err!', arguments)
            }).then(() => {
                this.isLoading = false
            })


        },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.remove-photo-btn {
    vertical-align: top;
    margin: -11px -24px;
    background-color: rgba(200,200,200,0.5);
}
</style>