<template>
    <div class="promo-page">
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-center card-container">
            <h1 class="top-header">Selling expertise? Make life easier.</h1>
            <h2 class="top-sub-header">Everything you need to run an instructional business, all in one place.</h2>
            <ul class="list-no-decor">
                <li><span><i class="fas fa-check-square"></i></span>Turnkey & Easy to use.</li>
                <li><span><i class="fas fa-check-square"></i></span>Your website, your brand.</li>
                <li><span><i class="fas fa-check-square"></i></span>Sets up in minutes. </li>
                <li><span><i class="fas fa-check-square"></i></span>Replaces 5 plus of software. </li>
                <li><span><i class="fas fa-check-square"></i></span>No need for plug-ins. </li>
                <li><span><i class="fas fa-check-square"></i></span>Free live support.</li>
                <li><span><i class="fas fa-check-square"></i></span>From $15 a month.</li>
            </ul>
            <div style="padding: 20px 0;">
                <b>Spend more time instructing and less on everything else.</b> Teachbeach makes it easy for experts to earn: 1. Set up in minutes. 2. Upload contacts. E. Invite to class.  4. Start earning
            </div>

            <div style="padding: 20px 0 10px">
                <div style="text-align: center;font-weight: bold;">14 days free!</div>
                <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start</span></v-btn>
            </div>
            <div><router-link to="/class/420">Join Us For A Live Demo</router-link></div>
            <v-card flat class="top-card">
                <v-card-title>
                    <div class="secondary-header text-xs-center">Your business before:<br/>Multiple platforms, plug-ins and log-ins</div>
                </v-card-title>
                <v-card-text>
                    <v-img
                        :aspect-ratio="16/9"
                        :src="beforeTB"
                    />
                </v-card-text>
            </v-card>
            <v-card flat class="top-card">
                <v-card-title>
                    <div class="secondary-header text-xs-center">
But your business after TeachBeach:<br/>
The world’s simplest dashboard <br/>
keeps you on track and organized!
                    </div>
                </v-card-title>
                <v-card-text>
                    <p>
                        Set it and forget. Your Turnkey Business-in-a-box sets up in minutes with an all- in-one dashboard that has everything and is actually fun to use.
                    </p>
                    <p>
                        <b>Use as your website… or integrate into an existing site with free live support.</b>  Your new tech team will implement domain redirect, transferring classes and customers, or integration with a different site.
                    </p>
                    <p>
                        <b>Test it free for 14 days. Here’s what you’ll  get:</b>
                    </p>
                </v-card-text>
            </v-card>
        </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-comet.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">Group and private session pricing optimized for good vibes</div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Trial offers</li>
                        <li>Drop-on rates </li>
                        <li>Package discounts</li>
                        <li>Membership options</li>
                        <li>Tracks credits used</li>
                        <li>Fixed date workshop or flexible sign-in</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-dreamy.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">Appointment scheduling made easy</div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Not available? No problem.</li>
                        <li>Customers can request a time from your schedule,  24/7 </li>
                        <li>Text to confirm or reschedule</li>
                        <li>Sync dates to your personal calendar</li>
                        <li>Easy for you, easy for them.</li>
                        <li>Automated reminders</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-alien.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">A CRM  to captures leads and save  time</div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Customers text you from the page</li>
                        <li>Contacts automatically saved to CRM</li>
                        <li>Upload existing contacts and customers, too</li>
                        <li>Email any group</li>
                        <li>“Invite to class” buttons with pre-filled link</li>
                        <li>Sign-in customers to tracks credits</li>
                        <li>Customer history </li>
                        <li>Free live support for migration</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-control.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">The small matter of getting paid, solved!</div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Super easy online payment</li>
                        <li>Stripe stores customers payment for future one click ordering</li>
                        <li>No need to talk about money, ever again.</li>
                        <li>Your chose: subscription, Prepaid, monthly, weekly, and/or per class payment</li>
                        <li>Refund button instantly solves tough customer issues.</li>
                        <li>Any  TeachBeach user can make a one cick order from any instructor</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-stars.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">Atuomated click-to-buy calendar </div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Customer-facing visual calendar shows all scheduled classes</li>
                        <li>Customers click on the time to enroll or sign-in</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-rocket.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">Marketing launched</div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Classes published in the Teachbeach local marketplace</li>
                        <li>Submitted automatically to ten plus community calendars</li>
                        <li>Includes TBT, Cl, Gabber, ILove the Burg, KeepStPete Local and neighbor calendars. </li>
                        <li>Easy share: Click to share any class on social media </li>
                        <li>Easy upload for email marketing:  Click to upload your contacts for text and email marketing </li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-sun.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">Business reports made simple</div>
                </v-card-title>
                <v-card-text>
                   <ul>
                       <li>View or export transactions and customers</li>
                       <li>Easily identify top earners and spenders</li>
                   </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 md6 class="text-xs-left card-container">
            <v-card class="card-item" flat>
                <div class="icon-container">
                    <img src="@/assets/promo-morty.svg" class="icon-image" />
                </div>
                <v-card-title>
                    <div class="card-header">Free live support</div>
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>Logo creation</li>
                        <li>Domain redirect </li>
                        <li>Integration with existing site </li>
                        <li>Help with class write-ups</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>
          <v-flex xs12 class="text-xs-center card-container">
              <div>
                  <b>Your serious about your passion. We are too. </b><br>
                       14 days free to try us out, including live support.
              </div>
              <div>
                  <v-btn depressed large class="platform-blgr" to="/teachers/company-or-individual" style="border-radius: 5px;height: 56px;"><span class="button-text">Start</span></v-btn>
              </div>
              <router-link to="/" style="text-decoration: none; color: black;">
                <img alt="Teachbeach. Keep learning" :src="defaultLogoSrc" style="height:72px;" to="/"/>
              </router-link>
          </v-flex>
      </v-layout>
    </div>
</template>

<script>
import metadata from '@/mixins/metadata'
import {defaultLogoSrc} from '@/store'

import promoAlien from '@/assets/promo-alien.svg'
import promoComet from '@/assets/promo-comet.svg'
import promoControl from '@/assets/promo-control.svg'
import promoDreamy from '@/assets/promo-dreamy.svg'
import promoMorty from '@/assets/promo-morty.svg'
import promoRocket from '@/assets/promo-rocket.svg'
import promoStars from '@/assets/promo-stars.svg'
import promoSun from '@/assets/promo-sun.svg'
import beforeTB from '@/assets/before-tb.png'

export default {
    mixins: [metadata],
    data: () => ({
        defaultLogoSrc,
        beforeTB,
    }),
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.promo-page {
    background-color: rgb(231, 231, 231);
    text-align: center;
    padding: 25px 132px;
    font-size: 24px;
}
    .top-header {
        font-size: 32px;
        font-weight: 600;
        text-align: center;
    }
    .top-sub-header {
        font-size: 20px;
        font-weight: 600;
        text-align: center;
    }
    .secondary-header {
        font-size: 1.6em;
        width: 100%;
        font-weight: 600;
    }
    .button-text {
        font-size: 24px;
    }
    .card-header {
        font-size: 1.34em;
        font-weight: 600;
    }
    .top-card {
        border-radius: 5px;
        margin-top: 25px;
    }
    .card-item {
        height: 100%;
        border-radius: 5px;
    }
    .card-container {
        padding: 32px 13px;

    }
    .icon-container {
        text-align: center;
        .icon-image {
            margin-top: -64px;
            margin-bottom: -10px;
            width: 128px;
            height: 128px;
        }
    }
    ul.list-no-decor {
      list-style: none;
      padding: 0;
        li > span {
          padding-right: 1.3em;
        }
    }
</style>