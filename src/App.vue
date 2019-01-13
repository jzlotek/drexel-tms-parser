<template>
  <v-app dark id="app">
    <v-alert
      :value="alert"
      type="error"
      transition="scale-transition"
      style="position: absolute"
    >
      {{ alertData }}
    </v-alert>

    <ClassSearch/>
    <ClassListing/>

    <WeekView :classesInput="[]"></WeekView>
  </v-app>
</template>

<script>
import VApp from 'vuetify/es5/components/VApp/VApp';
import EventBus from './EventBus';

/* webpackChunkName: "class-listing" */
const ClassListing = () => import('./components/ClassListing');
/* webpackChunkName: "class-search" */
const ClassSearch = () => import('./components/ClassSearch');
/* webpackChunkName: "week-view" */
const WeekView = () => import('./components/weekview/WeekView');
/* webpackChunkName: "v-alert" */
const VAlert = () => import('vuetify/es5/components/VAlert/VAlert');

export default {
  name: 'App',
  components: {
    VApp,
    ClassListing,
    ClassSearch,
    WeekView,
    VAlert,
  },
  data() {
    return {
      alert: false,
      alertData: null,
      obj: {
        course: {
          college: 'Antoinette Westphal COMAD', isQuarter: true, cn: '785', sc: 'AADM', it: 'Lecture', title: 'Research Design in the Arts', im: 'Online', cr: 3,
        },
        year: 18,
        semester: 'FA',
        crn: 13253,
        crnLink: 'https://termmasterschedule.drexel.edu/webtms_du/app?component=courseDetails2&page=CourseList&service=direct&sp=ZH4sIAAAAAAAAAFvzloG1uIhBPjWlVC%2BlKLUiNUcvs6hErzw1qSS3WC8lsSRRLyS1KJcBAhiZGJh9GNgTk0tCMnNTSxhEfLISyxL1iwtz9EECxSWJuQXWPgwcJUAtzvkpQBVCEBU5iXnp%2BsElRZl56TB5l9Ti5EKGOgamioKCEgY2IwNDC0NToAa3xJwchcDSxCKgIgVDC11DSwAnUj6JpAAAAA%3D%3D&sp=SA&sp=SAADM&sp=S13253&sp=S785&sp=0',
        sec: '900',
        meeting: { days: 'MWF', times: ['12:00:00', '12:50:00'] },
        instructor: 'Lindsey S Crane',
        maxEnroll: 0,
        enrolled: 0,
      },
    };
  },
  mounted() {
    EventBus.$on('error', (data) => {
      this.alert = true;
      this.alertData = data;
      setTimeout(() => { this.alert = false; }, 5000);
    });
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons");
@import "vuetify/dist/vuetify.min.css";
</style>
