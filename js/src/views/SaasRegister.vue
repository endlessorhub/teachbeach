<template>
    <section class="login-page-background">
        <div class="logo-div">
            <img src="@/assets/logo-blue.svg" />
        </div>
        <div class="login-form-div">
            <p class="form-heading">
                Looks like you're new here!
            </p>
            <p class="form-sub-heading">
                Let's get you started
            </p>
            <form>
                <div class="input-outer-div">
                    <div class="label-div"> <label for="email">Email ID</label></div>
                    <div class="input-div">
                        <input 
                            type="email" 
                            id="email"
                            name="email"
                            v-model.trim="email"
                            :error-messages="emailErrors"
                            required
                            @input="$v.email.$touch()"
                            @blur="$v.email.$touch()"
                        >
                    </div>
                </div>
                <div class="input-outer-div">
                    <div class="label-div"> <label for="password">Password</label></div>
                    <div class="input-div">
                        <input 
                            type="password" 
                            id="password" 
                            name="password"
                            browser-autocomplete="new-password"
                            v-model="password"
                            :error-messages="passwordErrors"
                            counter
                            label="Password"
                            required
                            @input="$v.password.$touch()"
                            @blur="$v.password.$touch()"
                        >
                    </div>
                </div>
                <div class="input-outer-div remember-me-div">
                    <div>
                        <input 
                            type="checkbox" 
                            id="remember-me" 
                            name="remember-me"
                            v-model="buildWebsite"
                        >
                        <label for="remember-me">Build a website</label>
                    </div>
                </div>
                <div class="login-btn-div">
                    <input type="submit" value="Register" @click="submit" />
                </div>
            </form>
        </div>
    </section>
</template>

<script>
import _ from 'lodash'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
import Timezone from '@/components/basic/Timezone'

export default {
    name: 'SaasRegister',
    mixins: [validationMixin],
    validations: {
        email: { required, email },
        password: { required, minLength: minLength(8) },
    },
    data: function () {
        return {
            email: this.$store.state.user ? this.$store.state.user.email : '',
            password: '',
            buildWebsite: false,
            isLoading: false,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            errors: {},
        }
    },
    computed: {
        alreadyRegistered: function () {
            return this.$store.state.user && this.$store.state.user.id ? true : false
        },
        emailErrors () {
            const errors = []
            if (this.errors.email) {
                return this.errors.email
            }
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.$v.email.required && errors.push('E-mail is required')
            return errors
        },
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push('Password is required')
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters long')
            return errors
        },
    },

    methods: {
        submit (event) {
            event.preventDefault();
            this.$v.$touch()
            //console.log('submit', this, arguments)
            if (this.$v.$anyError)
                return
            this.isLoading = true
            let _this = this
            axios.post('/api/users/', {
                email: this.email,
                password: this.password,
                timezone: this.timezone,
                is_company: this.buildWebsite,
            }).then(function (res) {
                //console.log(arguments)

                axios.get('/api/handshake/').then(function (initial) {
                    const params = new URLSearchParams();
                    params.append('username', res.data.email)
                    params.append('password', _this.password)
                    params.append('csrftoken', initial.data.csrftoken)
                    axios.post('/api/auth/login/', params).then((loginRes) => {
                        console.log(loginRes)
                        _this.$store.commit('setUser', _.omit(res.data, 'password'))
                        fbq('trackCustom', 'teacherWizard', {step: 'register'})
                        fbq('trackCustom', 'teacherRegistration')
                        if (_this.buildWebsite) _this.$router.push('/min-name-collab')
                        else _this.$router.push('/dashboard/teach/profile?main')
                    }).catch(function () {
                        console.log('err!', arguments)
                    }).then(() => {
                        _this.isLoading = false
                    })
                }).catch(function () {
                    //console.log(arguments)
                }).then(() => {

                })
            }).catch((err) => {
                ///handle errors
                _this.isLoading = false
                if (err.response.data) {
                    let errs = {}
                    _.each(err.response.data, (v, k) => {
                        if(k === 'email' && v.indexOf("User with this email already exists") !== -1) {
                            this.showLoginLink = true
                        }
                        errs[k] = v
                    })
                    _this.errors = errs
                }

            }).then(() => {
                //_this.isLoading = false
            })

        },
        clear () {
            this.$v.$reset()
            this.first_name = ''
            this.last_name = ''
            this.email = ''
            this.phone = ''
        }
    },
}
</script>
<style scoped>
.login-page-background {
  background-image: url("../assets/Group.png");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  width: 100%;
  height: 98vh;
  font-family: "Roboto", sans-serif;
  position: relative;
}
.login-page-background .logo-div {
  position: absolute;
  top: 26px;
  left: 170px;
  width: 217px;
}
@media (max-width: 1024px) {
  .login-page-background .logo-div {
    top: 20px;
    left: 70px;
  }
}
.login-page-background .login-form-div {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  max-width: 500px;
  width: 100%;
  height: -moz-fit-content;
  height: fit-content;
  margin: auto auto;
  padding: 80px 70px;
  background: #FFFFFF;
  box-shadow: 0px 0px 25px rgba(0, 0, 0, 0.35);
  border-radius: 8px;
  text-align: center;
}
@media (max-width: 1024px) {
  .login-page-background .login-form-div {
    padding: 60px 40px;
    max-width: 460px;
  }
}
@media (max-width: 768px) {
  .login-page-background .login-form-div {
    max-width: 300px;
    padding: 30px 20px;
  }
}
.login-page-background .login-form-div .form-heading {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 900;
  font-size: 32px;
  line-height: 38px;
  text-align: center;
  color: #111827;
  margin-bottom: 17px;
}
@media (max-width: 768px) {
  .login-page-background .login-form-div .form-heading {
    font-size: 24px;
  }
}
.login-page-background .login-form-div .form-sub-heading {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 500;
  font-size: 20px;
  line-height: 23px;
  text-align: center;
  color: #000000;
  margin-bottom: 44px;
}
@media (max-width: 768px) {
  .login-page-background .login-form-div .form-sub-heading {
    font-size: 16px;
  }
}
.login-page-background .login-form-div form .input-outer-div {
  text-align: left;
  margin-bottom: 20px;
}
.login-page-background .login-form-div form .input-outer-div .label-div {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 18px;
  color: #000000;
  margin-bottom: 6px;
}
.login-page-background .login-form-div form .input-outer-div .input-div input {
  width: 100%;
  background: #DDDDDD;
  border-radius: 50px;
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 18px;
  color: #000000;
  padding: 10px 0px 10px 6px;
  border: none;
  outline: none;
}
.login-page-background .login-form-div form .input-outer-div #remember-me {
  font-family: "Roboto", sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 12px;
  line-height: 13px;
  color: #000000;
}
.login-page-background .login-form-div form .login-btn-div {
  width: 100%;
  margin-top: 24px;
}
.login-page-background .login-form-div form .login-btn-div input {
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
.login-page-background .login-form-div form .remember-me-div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -10px;
}
.login-page-background .login-form-div form .remember-me-div a {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 400;
  font-size: 12px;
  line-height: 13px;
  color: #337BDD;
  text-decoration: none;
}
</style>