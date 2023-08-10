<template>
    <section class="name-collab-page-background">
        <div class="logo-div">
            <img src="@/assets/logo-blue.svg" />
        </div>
        <div class="name-collab-form-div">
            <p class="form-heading">
                Name your collab
            </p>
            <p class="form-sub-heading">
                If you are adding to an exisiting website use company name
            </p>
            <form>
                <div class="input-outer-div">
                    <div class="input-div"> <input v-model="name" type="text" id="name" name="name" placeholder="Name"></div>
                </div>
                <div class="input-outer-div">
                    <div class="label">
                        Upload
                    </div>
                    <div>
                        <image-upload-crop
                            :imageUrl="imageUrl"
                            :imageName="imageName"
                            :imageFile="imageFile"
                            width="100%"
                            :aspectRatio="1.25"
                            @change="onFileChanged"
                        />
                    </div>
                </div>

                <div class="login-btn-div">
                    <input 
                        type="submit" 
                        value="Next" 
                        @click="submit"
                        :disabled="isLoading"
                        :loading="isLoading"
                    />
                </div>
            </form>
        </div>
    </section>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'

export default {
    name: 'SaasNameCollab',
    components: {
        ImageUploadCrop,
    },
    data: () => ({
        isUpdated: false,
        isLoading: false,
        name: '',
        imageName: '',
        imageUrl: '',
		imageFile: '',
        crop: {},
    }),
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
        submit(e) {
            e.preventDefault();
            this.saveData()
            //make axios call
            this.isLoading = true
            axios.post('/api/company_profile/', {
                profile: {
                    companyName: this.name,
                    imageName: this.imageName,
                    imageUrl: this.imageUrl,
                    imageFile: this.imageFile,
                    mainImageName: this.imageName,
                    mainImageUrl: this.imageUrl,
                    mainImageFile: this.imageFile,
                },
                avatar: {
                    uploadPhoto: {
                        imageName: this.imageName,
                        imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                        imageFile: this.imageFile
                    }
                },
                main_media: {
                    uploadPhoto: {
                        imageName: this.imageName,
                        imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                        imageFile: this.imageFile,
                    },
                },
            }).then((res) => {
                this.$router.push('/dashboard/teach/profile?main')
            }).catch(() => {
                console.log('err!', arguments)
            }).then(() => {
                this.isLoading = false
            })
        },
        onFileChanged(e) {
            this.isUpdated = true
            this.imageName = e.imageName
            this.imageFile = e.imageFile
            this.imageUrl = e.imageUrl
            this.crop = e.crop
        },
    },
}
</script>
<style scoped>
.name-collab-page-background {
  font-family: "Roboto", sans-serif;
  position: relative;
  padding: 36px 80px;
}
@media (max-width: 1024px) {
  .name-collab-page-background {
    padding: 32px 60px;
  }
}
@media (max-width: 768px) {
  .name-collab-page-background {
    padding: 32px 36px;
  }
}
.name-collab-page-background .logo-div {
  margin-bottom: 70px;
  margin-left: 20px;
}
@media (max-width: 1024px) {
  .name-collab-page-background .logo-div {
    margin-bottom: 40px;
  }
}
.name-collab-page-background .name-collab-form-div {
  width: 100%;
  height: -moz-fit-content;
  height: fit-content;
  background: #FFFFFF;
  border-radius: 8px;
  text-align: left;
}
.name-collab-page-background .name-collab-form-div form {
  max-width: 500px;
}
.name-collab-page-background .name-collab-form-div .form-heading {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 900;
  font-size: 40px;
  line-height: 47px;
  color: #111827;
  margin-bottom: 49px;
  position: relative;
}
.name-collab-page-background .name-collab-form-div .form-heading::before {
  content: url("../assets/triangle.svg");
  position: absolute;
  left: -50px;
}
@media (max-width: 768px) {
  .name-collab-page-background .name-collab-form-div .form-heading::before {
    left: -35px;
    top: 5px;
  }
}
@media (max-width: 768px) {
  .name-collab-page-background .name-collab-form-div .form-heading {
    font-size: 28px;
    margin-bottom: 30px;
  }
}
.name-collab-page-background .name-collab-form-div .form-sub-heading {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 300;
  font-size: 23px;
  line-height: 27px;
  color: #000000;
  margin-bottom: 48px;
}
@media (max-width: 768px) {
  .name-collab-page-background .name-collab-form-div .form-sub-heading {
    font-size: 16px;
    margin-bottom: 42px;
  }
}
.name-collab-page-background .name-collab-form-div form .input-outer-div {
  text-align: left;
  margin-bottom: 45px;
}
@media (max-width: 768px) {
  .name-collab-page-background .name-collab-form-div form .input-outer-div {
    margin-bottom: 30px;
  }
}
.name-collab-page-background .name-collab-form-div form .input-outer-div .label {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 25px;
  line-height: 29px;
  color: #000000;
}
@media (max-width: 768px) {
  .name-collab-page-background .name-collab-form-div form .input-outer-div .label {
    font-size: 18px;
    line-height: 24px;
  }
}
.name-collab-page-background .name-collab-form-div form .input-outer-div .input-div input {
  width: 100%;
  background: transparent;
  border-radius: 0px;
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 25px;
  line-height: 29px;
  color: #000000;
  padding: 10px 0px;
  border: none;
  border-bottom: 2px solid #087AE1;
  outline: none;
}
@media (max-width: 768px) {
  .name-collab-page-background .name-collab-form-div form .input-outer-div .input-div input {
    font-size: 18px;
    line-height: 24px;
  }
}
.name-collab-page-background .name-collab-form-div form .input-outer-div #buttonid {
  margin-top: 5px;
  width: 100%;
  padding: 64px;
  background: rgba(221, 221, 221, 0.25);
  border-radius: 5px;
  border: none;
  outline: none;
}
.name-collab-page-background .name-collab-form-div form .login-btn-div {
  width: 100%;
  margin-top: 24px;
}
.name-collab-page-background .name-collab-form-div form .login-btn-div input {
  width: 100%;
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 500;
  font-size: 15px;
  line-height: 18px;
  text-align: center;
  color: #FFFFFF;
  padding: 11px;
  background: #337BDD;
  border-radius: 50px;
  border: none;
  outline: none;
}
</style>