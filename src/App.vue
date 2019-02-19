<template>
  <v-app id="app" dark>
    <v-toolbar color="primary" dark app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>Drexel TMS</v-toolbar-title>
    </v-toolbar>

    <v-content color="grey darken-2">
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
          <v-flex text-xs-center>
            <v-alert
              fixed
              :value="alert"
              type="error"
              transition="scale-transition"
              style="position: absolute"
            >
              {{ alertData }}
            </v-alert>

            <ClassSearch/>
            <ClassListing/>
            <v-calendar
              type="week"
              :firstInterval="7"
              :intervalCount="16"
              >
              <template
                slot="dayLabel"
                slot-scope="{ date, weekday }"
                >
                <div>
                  {{ date }}
                  {{ weekday }}
                </div>
              </template>
              <template
                slot="dayBody"
                slot-scope="{ date, timeToY, minutesToPixels, weekday }"
                >
                <template v-for="event in eventsMap[date]">
                  <div
                    v-if="event.time"
                    :key="event.title"
                    :style="{ top: timeToY(event.time) + 'px', height: minutesToPixels(event.duration) + 'px' }"
                    class="my-event with-time"
                    @click="open(event)"
                    v-html="event.title"
                  ></div>
                </template>
              </template>
            </v-calendar>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import VApp from 'vuetify/es5/components/VApp/VApp';
import EventBus from './EventBus';

/* webpackChunkName: "class-listing" */
const ClassListing = () => import('./components/ClassListing');
/* webpackChunkName: "class-search" */
const ClassSearch = () => import('./components/ClassSearch');

export default {
  name: 'App',
  components: {
    VApp,
    ClassListing,
    ClassSearch,
  },
  data() {
    return {
      alert: false,
      alertData: '',
    };
  },
  computed: {
    ...mapState({
      selected: state => state.selected,
    }),
    ...mapGetters({
      eventsMap: 'getMappedSelected',
    }),
  },
  mounted() {
    EventBus.$on('error', (data) => {
      this.alert = true;
      this.alertData = data;
      setTimeout(() => {
        this.alert = false;
        this.alertData = '';
      }, 5000);
    });
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons");
@import "vuetify/dist/vuetify.min.css";
</style>
